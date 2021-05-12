from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Venue, Artist, Note, Show
from ..forms import NewShowForm, NewNoteForm, CreateArtistForm, CreateVenueForm


def show_list(request):
    """ Displays all shows in db """
    shows = Show.objects.all().order_by('artist')
    return render(request, 'lmn/shows/show_list.html', {'shows': shows})


def show_detail(request, show_pk):
    """ Page for Show details """  # TODO: adding notes feature goes here
    show = get_object_or_404(Show, pk=show_pk)
    notes = Note.objects.filter(show=show_pk)
    return render(request, 'lmn/shows/show_detail.html', {'show': show, 'notes': notes})


def add_show_to_artist(request, artist_pk):
    """ From Artist details a Show can be added """
    artist = get_object_or_404(Artist, pk=artist_pk)
    venues = Venue.objects.all()
    create_venue_form = CreateVenueForm()
    return render(request, 'lmn/shows/add_show_to_artist.html', {'artist': artist, 'venues': venues, 'create_venue_form': create_venue_form})


def add_show_to_venue(request, venue_pk):
    """ From Venue details a Show can be added """
    venue = get_object_or_404(Venue, pk=venue_pk)
    artists = Artist.objects.all()
    create_artist_form = CreateArtistForm()
    return render(request, 'lmn/shows/add_show_to_venue.html', {'venue': venue, 'artists': artists,
                                                                'create_artist_form': create_artist_form})


def create_show(request):
    """ From whichever method used to creat show this method will pull all info together and get the Date """
    if request.method == 'POST':
        show_info = request.POST
        artist_pk = show_info.get('artist_pk')
        venue_pk = show_info.get('venue_pk')
        artist = get_object_or_404(Artist, pk=artist_pk)
        venue = get_object_or_404(Venue, pk=venue_pk)
        fields = {'artist': artist, 'venue': venue}
        form = NewShowForm(initial=fields)  # populates form with artist and venue info, leaving only date to be entered
        return render(request, 'lmn/shows/create_show.html', {'artist': artist, 'venue': venue, 'form': form})
    else:
        return render(request, 'lmn/shows/create_show.html')


def save_show(request):
    """ This method will do the saving once a Show has all fields, after checking to make sure it does not exist """
    if request.method == 'POST':
        form = NewShowForm(request.POST)
        show = form.save(commit=False)
        already_added = show_in_db(show.show_date, show.artist, show.venue)
        if not already_added and form.is_valid():
            show.save()
            messages.info(request, 'Show Saved')
            return redirect('show_list')
        else:
            messages.warning(request, 'Show already in database')
            return redirect('add_show_to_artist')
    else:
        return redirect('add_show_to_artist')  # a GET request will send the user to the add show to artist page


def show_in_db(date, artist, venue):
    """ checks if the show is already in db """
    show_date, show_artist, show_venue = [], [], []
    shows_in_db = Show.objects.all()
    for show in shows_in_db:
        show_date.append(show.show_date)
        show_artist.append(show.artist.name.upper())
        show_venue.append(show.venue.name.upper())
    if date in show_date and artist.name.upper() in show_artist and venue.name.upper() in show_venue:
        return True
    else:
        return False
