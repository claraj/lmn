from django.shortcuts import render

from ..models import Artist, Show
from ..forms import ArtistSearchForm
from ..paginator import paginate


def venues_for_artist(request, artist_pk):   # pk = artist_pk

    """ Get all of the venues where this artist has played a show """

    shows = Show.objects.filter(artist=artist_pk).order_by('-show_date')  # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    (shows, paginator, page) = paginate(request, shows, 10)

    return render(request, 'lmn/venues/venue_list_for_artist.html', { 'shows' : shows, 
                                                            'artist': artist,
                                                            'page_range': paginator.page_range, 
                                                            'num_pages' : paginator.num_pages, 
                                                            'current_page': page
                                                            })


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
    else:
        artists = Artist.objects.all().order_by('name')

    (artists, paginator, page) = paginate(request, artists, 10)

    return render(request, 'lmn/artists/artist_list.html', {'form': form, 
                                                            'search_term': search_name, 
                                                            'artists' : artists, 
                                                            'page_range': paginator.page_range, 
                                                            'num_pages' : paginator.num_pages, 
                                                            'current_page': page
                                                            })
