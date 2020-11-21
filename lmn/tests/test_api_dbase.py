
from lmn.views import views_admin

#imports below copied from test_views.py
#maybe don't need all...TBD
from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User
from django.db import IntegrityError
import re, datetime
from datetime import timezone



class TestTicketMasterAPI(TestCase):

    # def setUp(self):
    #     example_api_response = {
    #     "_embedded": {
        #     "events": [
        #         {"name": "George Strait",
        #        "dates": {
        #             "start": {
        #                 "localDate": "2021-07-31",
        #                 "localTime": "17:00:00",
        #                 "dateTime": "2021-07-31T22:00:00Z",
        #             },
        #         },
        #         "_embedded": {
        #             "venues": [
        #                 { "name": "U.S. Bank Stadium",
        #                 "city": { "name": "Minneapolis" },
        #                 "state": {  "name": "Minnesota", "stateCode": "MN",
        #                 }
        #                 }]}
        #         }]}}

        # #call method in views_admin,feeding the example response
        # #this should save data to the database
        # #views_admin.extract_music_details(example_api_response)
        # views_admin.get_music_data(example_api_response)
        
        #was data saved to dbase?  
    def test_save_artist_name_in_artist_table(self):
        artist1 = Artist(name='George Gershwin')
        artist1.save()
        artist.id
        
        #response = self.client.get( reverse('artist_list') , {'search_name' : 'George Strait'} )
        #self.assertContains(response, 'George Strait')
        #self.assertNotContains(response,'Queen' )


    def test_no_duplicate_artist_saved_to_dbase(self):
        artist1 = Artist(name='George Gershwin')
        artist1.save()
        artist2 = Artist(name = 'George Gershwin')
        with self.assertRaises(IntegrityError):
            artist2.save()
        

    def test_venue_saved(self):
        response = self.client.get( reverse('venue_list') , {'search_name' : 'U.S. Bank Stadium'} )
        self.assertContains(response, 'U.S. Bank Stadium')
        self.assertContains(response, 'MN')
       # self.assertContains(response, 'Minneapolis')
        self.assertNotContains(response, 'The Lounge')
        

    def test_no_duplicate_venue_saved_to_dbase(self):
        venue1 = Venue (name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN')
        venue1.save()
        venue2 = Venue(name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN')
        with self.assertRaises(IntegrityError):
            venue2.save()
        

    # def test_save_show(self):
    #    # self.fail()
    #    pass


    # def test_no_duplicate_show(self):
    #     artist3 = Artist(name = 'George Gershwin')
    #     artist3.save()
    #     artist3.id
    #     venue3 = Venue (name = 'U.S.A. Bank Stadium', city='Minneapolis', state = 'MN')
    #     venue3.save()
    #     venue3.id
        
    #     show3 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
    #     show3.save()
       
    #     #try to add a duplicate show
    #     show4 = Show(show_date='2021-07-31 22:00:00', artist = artist3, venue = venue3)
        
    #     with self.assertRaises(IntegrityError):
    #         show4.save()

        
        