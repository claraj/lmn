
from lmn.views import views_admin
from django.test import TestCase, Client
from django.urls import reverse
from lmn.models import Venue, Artist, Note, Show
from django.db import IntegrityError
import re, datetime
from datetime import timezone

'''Testing whether data is saved to database tables and constraints(unique 
and unique together) are enforced '''

class TestTicketMasterAPI(TestCase):
          
    def test_save_artist_name_to_artist_table(self):
        artist1 = Artist(name='George Gershwin')
        artist1.save()
        artist1.id 
        artist_count = Artist.objects.count()
        self.assertEqual(1, artist_count)
        self.assertEqual('George Gershwin', artist1.name)
        

    def test_no_duplicate_artist_saved_to_dbase(self):
        artist1 = Artist(name='George Gershwin')
        artist1.save()
        artist2 = Artist(name = 'George Gershwin')
        with self.assertRaises(IntegrityError):
            artist2.save()
        
    
    def test_venue_saved_to_database(self):
        venue1 = Venue(name='The Club', city = 'Salina', state = 'KS')
        venue1.save()
        venue1.id    #assigns id to object just saved
        venue_count = Venue.objects.count()
        self.assertEqual(1, venue_count)
        self.assertEqual(venue1.id, 1) #venue id is assigned


    def test_no_duplicate_venue_saved_to_dbase(self):
        venue1 = Venue(name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN')
        venue1.save()
        venue2 = Venue(name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN')
        with self.assertRaises(IntegrityError):
            venue2.save()
        

    def test_save_show(self):
        #need to save artist and venue and get their ids before can save a show
        artist3 = Artist(name = 'George Gershwin')
        artist3.save()
        artist3.id
        venue3 = Venue (name = 'U.S.A. Bank Stadium', city='Minneapolis', state = 'MN')
        venue3.save()
        venue3.id
        show3 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
        show3.save()
        self.assertEqual(show3.artist.name, 'George Gershwin')
        self.assertEqual(show3.venue.name, 'U.S.A. Bank Stadium')


    def test_no_duplicate_show_saved_to_dbase(self):
        artist3 = Artist(name = 'George Gershwin')
        artist3.save()
        artist3.id
        venue3 = Venue (name = 'U.S.A. Bank Stadium', city='Minneapolis', state = 'MN')
        venue3.save()
        venue3.id
        show3 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
        show3.save()
       
        #try to add a duplicate show
        show4 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
        with self.assertRaises(IntegrityError):
            show4.save()

        
        