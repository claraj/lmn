from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, EmptyPage


def venue_list(request):
    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        #search for this venue, display results
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')
    else:
        venues = Venue.objects.all().order_by('name')   # Todo paginate
    
    paginator = Paginator(venues, 2) # allows only 2 venues to be viewed per page

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        venues = paginator.page(page)
    except PageNotAnInteger:
        venues = paginator.page(1)
        page = 1
    except EmptyPage:
        venues = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'lmn/venues/venue_list.html', {'form': form, 'search_term': search_name, 
                    'venues' : venues, 'page_range': paginator.page_range, 'num_pages' : paginator.num_pages, 
                     'current_page': page})


def artists_at_venue(request, venue_pk):   # pk = venue_pk
    """ Get all of the artists who have played a show at the venue with pk provided """

    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date') 
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', { 'venue': venue, 'shows': shows })


def venue_detail(request, venue_pk):
    venue = get_object_or_404(Venue, pk=venue_pk)
    return render(request, 'lmn/venues/venue_detail.html' , { 'venue': venue })
