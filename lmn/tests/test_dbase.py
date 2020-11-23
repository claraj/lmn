
from django.test import TestCase, Client
from django.urls import reverse
from lmn.models import Venue, Artist, Note, Show
from django.db import IntegrityError
import re, datetime
from datetime import timezone
from lmn.views import views_admin
from lmn.views.views_admin import get_music_data, get_ticketMaster, extract_music_details


'''Testing whether data is saved to database tables and constraints(unique 
and unique together) are enforced '''

class TestTicketMasterAPI(TestCase):
          
    def test_save_to_database_from_api_call_response(self):
        mock_response = {
        "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
        "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }] }} ]}}
        #calling this method with the mock response should result in data being saved to the database
        extract_music_details(mock_response)
        
        artist_count = Artist.objects.count()
        self.assertEqual(1, artist_count)
        artist_1 = Artist.objects.get(pk=1)
        self.assertEqual(artist_1.name, 'George Strait')
        venue_count = Venue.objects.count()
        venue_1 = Venue.objects.get(pk=1)
        self.assertEqual(venue_1.name, 'U.S. Bank Stadium')
        self.assertEqual(venue_1.state, 'MN')
        self.assertEqual(1, venue_count)
        show_count = Show.objects.count()
        self.assertEqual(1, show_count)
        show_1 = Show.objects.get(pk=1)
        self.assertEqual(show_1.artist.name, 'George Strait')


    def test_no_duplicate_artist_saved_to_dbase(self):
        artist1 = Artist(name='George Gershwin')
        artist1.save()
        artist2 = Artist(name = 'George Gershwin')
        with self.assertRaises(IntegrityError):
            artist2.save()
        

    def test_no_duplicate_venue_saved_to_dbase(self):
        venue1 = Venue(name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN')
        venue1.save()
        venue2 = Venue(name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN')
        with self.assertRaises(IntegrityError):
            venue2.save()
        

    def test_no_duplicate_show_saved_to_dbase(self):
        artist3 = Artist(name = 'George Gershwin')
        artist3.save()
        artist3.id
        venue3 = Venue (name = 'U.S.A. Bank Stadium', city='Minneapolis', state = 'MN')
        venue3.save()
        venue3.id
        show3 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
        #show3.show_date.isoformat()
        show3.save()
        #try to add a duplicate show
        show4 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
        with self.assertRaises(IntegrityError):
            show4.save()

        
