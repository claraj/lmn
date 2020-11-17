
import unittest
from unittest import TestCase
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

    def test_retrieve_data(self):
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

        # expected_result = [
        #     {"performer": "George Strait",
        #     "venueName": "U.S Bank Stadium",
        #      "venueCity": "Minneapolis",
        #      "venueState": "MN",
        #      "show_date_time": "2021-07-31T22:00:00Z"
        #     }
        # ]

        #call method in views_admin,feeding the example response
        views_admin.get_music_data(example_api_response)
        #method returns 200 if successful. 
        #  
        #data saved to test dbase? - need a dummy dbase?
        #then make sure artist.name="George Strait"
            #venue.name = .... etc?

        