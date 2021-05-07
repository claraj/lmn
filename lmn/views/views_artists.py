from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ArtistForm
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


def artist_list(request):  # pagination made possible by a ridiculously deep rabbit hole of docs and tutorials
    form = ArtistSearchForm()  # most notable was prob Corey Schafer
    search_name = request.GET.get('search_name')  # (https://www.youtube.com/channel/UCCezIgC97PvUuR4_gbFUs5g)
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
    return render(request, 'lmn/artists/artist_detail.html', {'artist': artist})


def add_artist(request):
    if request.method == 'POST':
        new_artist_form = ArtistForm(request.POST)
        if new_artist_form.is_valid():
            search_artist = new_artist_form.cleaned_data['name']  # grabs the entered name to use as a search term
            search_results = search_mb_artist_by_name(search_artist)  # returns a list of artist objects from api
            if search_results:
                return render(request, 'lmn/artists/save_artist.html', {'search_results': search_results})
            # else:
    new_artist_form = ArtistForm()
    return render(request, 'lmn/artists/add_artist.html', {'new_artist_form': new_artist_form})


def save_artist(request):
    if request.method == 'POST':
        new_artist = request.POST  # takes in info from the template and creates a new artist object
        new_name = new_artist.get('name')
        new_hometown = new_artist.get('hometown')
        new_desc = new_artist.get('description')
        artist = Artist(name=new_name, hometown=new_hometown, description=new_desc)
        already_added = artist_in_db(new_name, new_desc)
        if not already_added:
            print('safe to add!')
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
            return render(request, 'lmn/artists/save_artist.html')  # redirects back to add page so user can correct

    else:
        return render(request, 'lmn/artists/save_artist.html')


def artist_in_db(name, description):
    artist_name, artist_desc = [], []
    artists_in_db = Artist.objects.all()
    for artist in artists_in_db:
        artist_name.append(artist.name.upper())
        artist_desc.append(artist.description.upper())
    if name.upper() in artist_name and description.upper() in artist_desc:
        return True
    else:
        return False
