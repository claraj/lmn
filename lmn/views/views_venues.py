from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from ..api_calls import search_mb_place
from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, VenueForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def venue_list(request):
    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        #search for this venue, display results
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')
    else :
        venues = Venue.objects.all().order_by('name')   # Todo paginate

    return render(request, 'lmn/venues/venue_list.html', { 'venues': venues, 'form': form, 'search_term': search_name })


def artists_at_venue(request, venue_pk):   # pk = venue_pk
    """ Get all of the artists who have played a show at the venue with pk provided """

    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date') 
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', { 'venue': venue, 'shows': shows })


def venue_detail(request, venue_pk):
    venue = get_object_or_404(Venue, pk=venue_pk)
    return render(request, 'lmn/venues/venue_detail.html' , { 'venue': venue })


def add_venue(request):
    if request.method == 'POST':
        new_venue_form = VenueForm(request.POST)
        if new_venue_form.is_valid():
            search_venue = new_venue_form.cleaned_data['name']  # grabs the entered name to use as a search term
            search_results = search_mb_place(search_venue)  # returns a list of artist objects from api
            for a in search_results:
                print(a)  # for testing, prints every returned artist to terminal TODO delete when not needed
            try:
                new_venue_form.save()  # still currently saving whatever is entered (user data, not api)
                messages.info(request, 'Venue Saved')
                return redirect('venue_list')
            except ValidationError:
                messages.warning(request, 'Not a valid Venue')
                return redirect(request, 'add_venue')  # redirects back to add page so user can correct

            except IntegrityError:
                messages.warning(request, 'Venue already in database')
        else:
            return render(request, 'lmn/venues/add_venue.html', {'new_venue_form': new_venue_form})
    new_venue_form = VenueForm()
    return render(request, 'lmn/venues/add_venue.html', {'new_venue_form': new_venue_form})
