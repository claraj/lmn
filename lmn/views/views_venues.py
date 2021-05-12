from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from ..api_calls import search_mb_place
from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, VenueForm, CreateVenueForm, \
    CreateArtistForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError


def venue_list(request):  # pagination made possible by a ridiculously deep rabbit hole of docs and tutorials
    form = VenueSearchForm()  # most notable was prob Corey Schafer
    search_name = request.GET.get('search_name')  # (https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g)
    page = request.GET.get('page')  # page query
    if search_name:
        # search for this venue, display results
        venues_list = Venue.objects.filter(name__icontains=search_name).order_by('name')
        paginator = Paginator(venues_list, 6)  # creates a paginator that will chop up the list into pages
        try:
            venues = paginator.page(page)  # gets the number of pages from paginator
        except PageNotAnInteger:
            venues = paginator.page(1)  # if the page is not an integer, deliver the first page
        except EmptyPage:
            venues = paginator.page(paginator.num_pages)  # if the page is out of range, deliver the last page
    else:
        venues_list = Venue.objects.all().order_by('name')
        paginator = Paginator(venues_list, 6)
        try:
            venues = paginator.page(page)
        except PageNotAnInteger:
            venues = paginator.page(1)
        except EmptyPage:
            venues = paginator.page(paginator.num_pages)

    return render(request, 'lmn/venues/venue_list.html', {'venues': venues, 'form': form, 'search_term': search_name})


def artists_at_venue(request, venue_pk):  # pk = venue_pk
    ''' Get all of the artists who have played a show at the venue with pk provided '''
    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date')
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', {'venue': venue, 'shows': shows})


def venue_detail(request, venue_pk):
    venue = get_object_or_404(Venue, pk=venue_pk)

    return render(request, 'lmn/venues/venue_detail.html', {'venue': venue})


def add_venue(request):
    ''' this begins the process of adding a venue by calling the API '''
    if request.method == 'POST':
        new_venue_form = VenueForm(request.POST)
        if new_venue_form.is_valid():
            search_venue = new_venue_form.cleaned_data['name']  # grabs the entered name to use as a search term
            search_results = search_mb_place(search_venue)  # returns a list of artist objects from api
            if search_results:
                create_venue_form = CreateVenueForm()
                return render(request, 'lmn/venues/save_venue.html', {'search_results': search_results,
                                                                      'create_venue_form': create_venue_form})
            else:
                messages.info(request, 'No results for that venue')
                create_venue_form = CreateVenueForm()
                return render(request, 'lmn/venues/save_venue.html', {'search_results': search_results,
                                                                      'create_venue_form': create_venue_form})
    new_venue_form = VenueForm()

    return render(request, 'lmn/venues/add_venue.html', {'new_venue_form': new_venue_form})


def save_venue(request):
    ''' once an venue result from api or newly entered venue is selected
     this method will check to see if it should/can be saved and if so, saves it '''
    if request.method == 'POST':
        new_venue = request.POST
        new_name = new_venue.get('name')
        new_address = new_venue.get('address')
        venue = Venue(name=new_name, address=new_address)
        already_added = venue_in_db(new_name, new_address)
        if not already_added:
            try:
                venue.save()
                messages.info(request, 'Venue Saved')
                return redirect('venue_list')
            except ValidationError:
                messages.warning(request, 'Not a valid Venue')
                return redirect(request, 'add_venue')  # redirects back to add page so user can correct
            except IntegrityError:
                messages.warning(request, 'Venue already in database')
                return redirect('add_venue')
        else:
            messages.warning(request, 'Venue already in database')
            return redirect('add_venue')
    else:
        return redirect('add_venue')


def create_venue(request):
    ''' if api results are not what the user needs, they can enter a new venue '''
    if request.method == 'POST':
        form = CreateVenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
        else:
            messages.warning(request, 'Address is already Registered, or Form Invalid. Please try again')
            return redirect('add_venue')

        already_added = venue_in_db(venue.name, venue.address)
        if not already_added:
            try:
                venue.save()
                messages.info(request, 'Venue Saved')
                return redirect('venue_list')
            except ValidationError:
                messages.warning(request, 'Not a valid Venue')
                return redirect(request, 'add_venue')  # redirects back to add page so user can correct
            except IntegrityError:
                messages.warning(request, 'Venue already in database')
                return redirect('add_venue')
        else:
            messages.warning(request, 'Venue or Venue address already in database')
            return redirect('add_venue')
    else:
        return redirect('add_venue')  # a GET request will send the user to the add venue page


def venue_in_db(name, address):
    ''' checks if the venue is already in db based on name and description '''
    venue_name, venue_address = [], []
    venues_in_db = Venue.objects.all()
    for venue in venues_in_db:
        venue_name.append(venue.name.upper())
        venue_address.append(venue.address.upper())
    if name.upper() in venue_name and address.upper() in venue_address:
        return True
    else:
        return False
