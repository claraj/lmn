from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ArtistForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone


def venues_for_artist(request, artist_pk):   # pk = artist_pk

    """ Get all of the venues where this artist has played a show """

    shows = Show.objects.filter(artist=artist_pk).order_by('-show_date')  # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', { 'artist': artist, 'shows': shows })


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
    else:
        artists = Artist.objects.all().order_by('name')

    return render(request, 'lmn/artists/artist_list.html', { 'artists': artists, 'form': form, 'search_term': search_name })


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    return render(request, 'lmn/artists/artist_detail.html' , { 'artist': artist })


def add_artist(request):
    if request.method == 'POST':
        new_artist_form = ArtistForm(request.POST)
        if new_artist_form.is_valid():
            new_artist_form.save()
            # todo show success message or redirect to list of artist
        else:
            return render(request, 'lmn/artists/add_artist.html', {'new_artist_form': new_artist_form})
    new_artist_form = ArtistForm()    
    return render(request, 'lmn/artists/add_artist.html', {'new_artist_form': new_artist_form})