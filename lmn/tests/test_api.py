
#import unittest
#from unittest import TestCase
from lmn.views import views_admin

#imports below copied from test_views.py
#do I not need unittest?
from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User

import re, datetime
from datetime import timezone



class TestTicketMasterAPI(TestCase):

    def setUp(self):
        example_api_response = {
        "_embedded": {
            "events": [
                {
                "name": "George Strait",
                "type": "event",
                "url": "https://www.ticketmaster.com/george-strait-minneapolis-minnesota-07-31-2021/event/06005830D6D4864F",
                "dates": {
                    "start": {
                        "localDate": "2021-07-31",
                        "localTime": "17:00:00",
                        "dateTime": "2021-07-31T22:00:00Z",
                    },
                "timezone": "America/Chicago",
                },
                
                "_embedded": {
                    "venues": [
                        {
                        "name": "U.S. Bank Stadium",
                        "type": "venue",
                        "postalCode": "55415",
                        "timezone": "America/Chicago",
                        "city": {
                            "name": "Minneapolis"
                        },
                        "state": {
                            "name": "Minnesota",
                            "stateCode": "MN",
                        }
                        }]}
                }]}}

        #call method in views_admin,feeding the example response
        #this should save data to the database
        views_admin.extract_music_details(example_api_response)
    
        
        #was data saved to dbase?  
    def test_save_artist_name_in_artist_table(self):
        response = self.client.get( reverse('artist_list') , {'search_name' : 'George Strait'} )
        self.assertContains(response, 'George Strait')
        self.assertNotContains(response,'Queen' )


    def test_venue_saved(self):
        response = self.client.get( reverse('venue_list') , {'search_name' : 'U.S. Bank Stadium'} )
        self.assertContains(response, 'U.S. Bank Stadium')
        self.assertContains(response, 'MN')
        self.assertContains(response, 'Minneapolis')
        self.assertNotContains(response, 'The Lounge')
        self.assertNotContains(response, 'Kansas City')
        self.assertNotContains(response, 'KS')

    #def test_show_date_saved(self):

    # to test unique together constraint- so can't add duplicate show
    # def test_unique_together(self):
    #     example_api_response = {
    #     "_embedded": {
    #         "events": [
    #             {
    #             "name": "George Strait",
    #             "type": "event",
    #             "url": "https://www.ticketmaster.com/george-strait-minneapolis-minnesota-07-31-2021/event/06005830D6D4864F",
    #             "dates": {
    #                 "start": {
    #                     "localDate": "2021-07-31",
    #                     "localTime": "17:00:00",
    #                     "dateTime": "2021-07-31T22:00:00Z",
    #                 },
    #             "timezone": "America/Chicago",
    #             },
                
    #             "_embedded": {
    #                 "venues": [
    #                     {
    #                     "name": "U.S. Bank Stadium",
    #                     "type": "venue",
    #                     "postalCode": "55415",
    #                     "timezone": "America/Chicago",
    #                     "city": {
    #                         "name": "Minneapolis"
    #                     },
    #                     "state": {
    #                         "name": "Minnesota",
    #                         "stateCode": "MN",
    #                     }
    #                     }]}
    #             }]}}

    #     #call method in views_admin,feeding the example response
    #     #this should save data to the database
    #     views_admin.extract_music_details(example_api_response)

    #     response = self.client.get(reverse('artist_list'))
    #     self.assertEqual(len(response.context['artists']), 1)


    
        