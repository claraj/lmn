from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ArtistForm, SaveArtistForm
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
            new_artist_form = ArtistForm()
            return render(request, 'lmn/artists/add_artist.html', {'search_results': search_results})


            # for a in search_results:
            #     print(a)  # for testing, prints every returned artist to terminal TODO delete when not needed
            # try:
            #     new_artist_form.save()  # still currently saving whatever is entered (user data, not api)
            #     messages.info(request, 'Artist Saved')
            #     return redirect('artist_list')
            # except ValidationError:
            #     messages.warning(request, 'Not a valid Artist')
            #     return redirect(request, 'add_artist')  # redirects back to add page so user can correct

        #     except IntegrityError:
        #         messages.warning(request, 'Artist already in database')
        # else:
        #     return render(request, 'lmn/artists/add_artist.html', {'new_artist_form': new_artist_form})
    new_artist_form = ArtistForm()
    return render(request, 'lmn/artists/add_artist.html', {'new_artist_form': new_artist_form})



def save_artist(request, artist):
    if request.method == 'POST':
        artist =
        if new_artist_form.is_valid():
            print(artist.name)