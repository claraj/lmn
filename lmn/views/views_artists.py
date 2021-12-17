from django.shortcuts import render, get_object_or_404

from ..models import Artist, Show
from ..forms import ArtistSearchForm


def venues_for_artist(request, artist_pk):
    """ Get all of the venues where this artist has played a show """
    shows = Show.objects.filter(artist=artist_pk).order_by('-show_date')  # most recent first
    artist = Artist.objects.get(pk=artist_pk)
    return render(request, 'lmn/venues/venue_list_for_artist.html', {'artist': artist, 'shows': shows})


def artist_list(request):
    """ Get a list of all artists, ordered by name.

    If request contains a GET parameter search_name then 
    only include artists with names containing that text. """
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
    else:
        artists = Artist.objects.all().order_by('name')

    return render(request, 'lmn/artists/artist_list.html', {'artists': artists, 'form': form, 'search_term': search_name})


def artist_detail(request, artist_pk):
    """ Get details about one artist """
    artist = get_object_or_404(Artist, pk=artist_pk)
    return render(request, 'lmn/artists/artist_detail.html', {'artist': artist})
