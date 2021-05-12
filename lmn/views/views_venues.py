from ..models import Venue, Show
from ..forms import VenueSearchForm
from ..paginator import paginate

from django.shortcuts import render


def venue_list(request):
    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        #search for this venue, display results
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')
    else:
        venues = Venue.objects.all().order_by('name')   # Todo paginate
    
    (venues, paginator, page) = paginate(request, venues, 10)

    return render(request, 'lmn/venues/venue_list.html', {'form': form, 
                                                          'search_term': search_name, 
                                                          'venues' : venues, 
                                                          'page_range': paginator.page_range, 
                                                          'num_pages' : paginator.num_pages, 
                                                          'current_page': page})


def artists_at_venue(request, venue_pk):   # pk = venue_pk
    """ Get all of the artists who have played a show at the venue with pk provided """

    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date') 
    venue = Venue.objects.get(pk=venue_pk)

    (shows, paginator, page) = paginate(request, shows, 10)

    return render(request, 'lmn/artists/artist_list_for_venue.html', { 'venue': venue, 
                                                                       'shows': shows, 
                                                                       'page_range': paginator.page_range, 
                                                                       'num_pages' : paginator.num_pages, 
                                                                       'current_page': page
                                                                       })            
