
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

    def setUp(self):
        example_api_response = {
        "_embedded": {
            "events": [
                {"name": "George Strait",
               "dates": {
                    "start": {
                        "localDate": "2021-07-31",
                        "localTime": "17:00:00",
                        "dateTime": "2021-07-31T22:00:00Z",
                    },
                },
                "_embedded": {
                    "venues": [
                        { "name": "U.S. Bank Stadium",
                        "city": { "name": "Minneapolis" },
                        "state": {  "name": "Minnesota", "stateCode": "MN",
                        }
                        }]}
                }]}}

        #call method in views_admin,feeding the example response
        #this should save data to the database
        #views_admin.extract_music_details(example_api_response)
        views_admin.get_music_data(example_api_response)
        
        #was data saved to dbase?  
    def test_save_artist_name_in_artist_table(self):
        response = self.client.get( reverse('artist_list') , {'search_name' : 'George Strait'} )
        self.assertContains(response, 'George Strait')
        self.assertNotContains(response,'Queen' )


    def test_no_duplicate_artist(self):
        #set up loads artist George Strait
        
        artist = Artist(name = 'George Strait')
        artist.save()
        artist2 = Artist(name = 'George Strait')
        artist2.save()

        #performer = 'George Strait'
        #artist = Artist(name = performer)
        #artist.save() #try to save artist, but since unique constraint, will not save
        
        self.assertRaises(IntegrityError)


    def test_venue_saved(self):
        response = self.client.get( reverse('venue_list') , {'search_name' : 'U.S. Bank Stadium'} )
        self.assertContains(response, 'U.S. Bank Stadium')
        self.assertContains(response, 'MN')
       # self.assertContains(response, 'Minneapolis')
        self.assertNotContains(response, 'The Lounge')
        

    # def test_no_duplicate_venue(self):
    #     initial_venue_count= Venue.objects.count()
    #     print('initial venue count', initial_venue_count)
    #     venue = Venue(name = 'U.S. Bank Stadium', city='Minneapolis', state = 'MN').save()
    #     current_venue_count = Venue.objects.count()
    #     #counts should be the same as venue is a duplicate and should not be added
    #     self.assertEqual(initial_venue_count,current_venue_count)


    # def test_save_show(self):
    #    # self.fail()
    #    pass


    # def test_no_duplicate_show(self):
    #     initial_show_count= Show.objects.count()
    #     print('showCount', initial_show_count)
    #     #try to add a duplicate show
    #     show = Show(show_date='2021-07-31 22:00:00' , artist ='George Strait' ,venue = 'U.S. Bank Stadium').save()
    #     new_show_count = Show.objects.count()
    #     #show should not add to dbase because not unique, so count stays same
    #     self.assertEqual(initial_show_count, new_show_count)