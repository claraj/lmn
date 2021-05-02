from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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

    return render(request, 'lmn/venues/venue_list.html', { 'venues': venues, 'form': form, 'search_term': search_name })


def artists_at_venue(request, venue_pk):   # pk = venue_pk
    """ Get all of the artists who have played a show at the venue with pk provided """

    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date') 
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', { 'venue': venue, 'shows': shows })


def venue_detail(request, venue_pk):
    venue = get_object_or_404(Venue, pk=venue_pk)
    return render(request, 'lmn/venues/venue_detail.html' , { 'venue': venue })
