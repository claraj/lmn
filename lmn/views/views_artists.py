from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, EmptyPage

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

    paginator = Paginator(artists, 10) # allows only 10 artists to be viewed per page

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        artists = paginator.page(page)
    except PageNotAnInteger:
        artists = paginator.page(1)
        page = 1
    except EmptyPage:
        artists = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'lmn/artists/artist_list.html', {'form': form, 'search_term': search_name, 
                    'artists' : artists, 'page_range': paginator.page_range, 'num_pages' : paginator.num_pages, 
                     'current_page': page})


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    return render(request, 'lmn/artists/artist_detail.html' , { 'artist': artist })
