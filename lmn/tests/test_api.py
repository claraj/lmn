import requests
import unittest

from unittest import TestCase
from unittest import mock
from ..models import Artist, Venue, Show

from lmn.views.views_admin import get_music_data, get_ticketMaster, extract_music_details


#with guidance from  Hugh's api testing in wishful...
def mock_requests_get(url, params):
    class MockAPI:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if params['classificationName'] == 'music' and params['city'] == 'Minneapolis':
        return MockAPI({
        "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
        "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }]}}]}})
        
    return MockAPI

class TestTickemasterAPI(TestCase):
        #when patching, return side_effect instead of real request.get from API
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch(self, mock_get):
            #assert requests.get call returns this response
        mock_response = {
    "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
    "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }] }} ]}}
        params = ('music', 'minneapolis')
        
        data=get_ticketMaster() #call method in views_admin.py
        
        self.assertEqual(mock_response, data)
        

