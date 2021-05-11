from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ArtistForm, CreateArtistForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from lmn.api_calls import search_mb_artist_by_name
from django.utils import timezone


def venues_for_artist(request, artist_pk):  # pk = artist_pk

    """ Get all of the venues where this artist has played a show """

    shows = Show.objects.filter(artist=artist_pk).order_by('-show_date')  # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', {'artist': artist, 'shows': shows})


""" pagination made possible by a ridiculously deep rabbit hole of docs and tutorials pagination
 made possible by a ridiculously deep rabbit hole of docs and tutorials 
 (https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g) """


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    page = request.GET.get('page')  # page query
    if search_name:
        artists_list = Artist.objects.filter(name__icontains=search_name).order_by('name')
        paginator = Paginator(artists_list, 6)  # creates a paginator that will chop up the list into pages
        try:
            artists = paginator.page(page)  # gets the number of pages from paginator
        except PageNotAnInteger:
            artists = paginator.page(1)  # if the page is not an integer, deliver the first page
        except EmptyPage:
            artists = paginator.page(paginator.num_pages)  # if the page is out of range, deliver the last page
    else:
        artists_list = Artist.objects.all().order_by('name')
        paginator = Paginator(artists_list, 6)
        try:
            artists = paginator.page(page)
        except PageNotAnInteger:
            artists = paginator.page(1)
        except EmptyPage:
            artists = paginator.page(paginator.num_pages)

    return render(request, 'lmn/artists/artist_list.html',
                  {'artists': artists, 'form': form, 'search_term': search_name})


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    shows = Show.objects.filter(artist=artist_pk).order_by('venue')
    form = VenueSearchForm()
    return render(request, 'lmn/artists/artist_detail.html', {'artist': artist, 'shows': shows, 'form': form})


def add_artist(request):
    """ this begins the process of adding an artist by calling the API """
    if request.method == 'POST':
        new_artist_form = ArtistForm(request.POST)
        if new_artist_form.is_valid():
            search_artist = new_artist_form.cleaned_data['name']  # grabs the entered name to use as a search term
            search_results = search_mb_artist_by_name(search_artist)  # returns a list of artist objects from api
            if search_results:
                create_artist_form = CreateArtistForm()
                return render(request, 'lmn/artists/save_artist.html', {'search_results': search_results,
                                                                        'create_artist_form': create_artist_form})
            # else:
    new_artist_form = ArtistForm()
    return render(request, 'lmn/artists/add_artist.html', {'new_artist_form': new_artist_form})


def save_artist(request):
    """ once an artist result from api or newly entered artist is selected
     this method will check to see if it should/can be saved and if so, saves it """
    if request.method == 'POST':
        new_artist = request.POST  # takes in info from the template and creates a new artist object
        new_name = new_artist.get('name')
        new_hometown = new_artist.get('hometown')
        new_desc = new_artist.get('description')
        artist = Artist(name=new_name, hometown=new_hometown, description=new_desc)
        already_added = artist_in_db(new_name, new_hometown, new_desc)
        if not already_added:
            try:
                artist.save()  # try except block to determine if artist can be saved
                messages.info(request, 'Artist Saved')
                return redirect('artist_list')
            except ValidationError:
                messages.warning(request, 'Not a valid Artist')
                return redirect(request, 'add_artist')  # redirects back to add page so user can correct
            except IntegrityError:
                messages.warning(request, 'Artist already in database')

        else:
            messages.warning(request, 'Artist already in database')
            return redirect('add_artist')
    else:
        return redirect('add_artist')  # a GET request will send the user to the add artist page


def create_artist(request):
    """ if api results are not what the user needs, they can enter a new artist """
    if request.method == 'POST':
        form = CreateArtistForm(request.POST)
        artist = form.save(commit=False)
        already_added = artist_in_db(artist.name, artist.hometown, artist.description)
        if not already_added and form.is_valid():
            artist.save()
            messages.info(request, 'Artist Saved')
            return redirect('artist_list')
        else:
            messages.warning(request, 'Artist already in database')
            return redirect('add_artist')
    else:
        return redirect('add_artist')  # a GET request will send the user to the add artist page


def artist_in_db(name, hometown, description):
    """ checks if the artist is already in db based on name and description """
    artist_name, artist_home, artist_desc = [], [], []
    artists_in_db = Artist.objects.all()
    for artist in artists_in_db:
        artist_name.append(artist.name.upper())
        artist_home.append(artist.hometown.upper())
        artist_desc.append(artist.description.upper())
    if name.upper() in artist_name and hometown.upper() in artist_home and description.upper() in artist_desc:
        return True
    else:
        return False
