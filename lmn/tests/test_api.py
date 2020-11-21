import requests
import unittest
#?? I thought I had to use django.test import TestCase??
from unittest import TestCase
from unittest import mock
from ..models import Artist, Venue, Show

from lmn.views.views_admin import get_music_data, extract_music_details


def mock_requests_get(url, params):
    class MockAPI:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data
#query= {'classificationName': classificationName, 'city' : city, 'apikey': key}
        
    if params['classificationName'] == 'music' and params['city'] == 'Minneapolis':
        return MockAPI({
        "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
        "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }]}}]}})
        #try again
        #return MockAPI({"_embedded": {"events": [{"name": "George Strait","dates": {"start": {"dateTime": "2021-07-31T22:00:00Z",},},
         #   "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": {"name": "Minneapolis"},"state": {"stateCode": "MN"},}],}}

    return MockAPI(None)  #???

class TestTickemasterAPI(TestCase):
        #when patching, return side_effect instead of real request.get from API
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch(self, mock_get):
            #assert requests.get call returns this response
        mock_response = {
    "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
    "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }] }} ]}}
        params = ('music', 'minneapolis')
        error, data =get_music_data( params)
        self.assertIsNone(error)
        self.assertEqual(mock_response, data)

#was data saved to dbase? 
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_save_artist_name_in_artist_table(self, mock_get):
        mock_response = {"_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
    "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }] }} ]}}
        #artist_name = 'George Strait'
        #details = extract_music_details(mock_response)
        extract_music_details(mock_response) #should save info to dbase
        #below can only be used with django test case
        #response = self.client.get(reverse('artist_list') , {'search_name' : 'George Strait'} )
        
        artist_1 = Artist.objects.get(pk=1)
        self.assertEqual( artist_1.name, 'George Strait')
        
        


    # def test_retrieve_artist(self):
    #     mock_response = {
    #     "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
    #     "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }]}}]}}
    # #feed the mock response to the extract_music_details function
    #     data = extract_music_details(mock_response)
        
    #     self.assertEqual('George Strait', data.artist.name)

#was data saved to dbase? 
        # def test_save_artist_name_in_artist_table(self):
        #     response = self.client.get( reverse('artist_list') , {'search_name' : 'George Strait'} )
        #     self.assertContains(response, 'George Strait')
        #     self.assertNotContains(response,'Queen' )





