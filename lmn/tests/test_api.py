import requests
import unittest

from unittest import TestCase
from unittest import mock
from ..models import Artist, Venue, Show

from lmn.views.views_admin import get_music_data


# class TestTickemasterAPI(TestCase):
# #like slide 37 ontest_exchange_rates.py-Testing22 powerpoint
#     @patch('get_music_data')
#     def test_get_data_from_ticketmaster(self)
#         #mock_venue_name = 'U.S. Bank Stadium'
#         example_api_response= {
#           "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
#          "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }]}}]}}
#         mock_venue_name.side_effect = [ example_api_response]
#         #this method only used if get_music_data is split into 2 fxs
#         get_music_data(params)
#         ?= extract_music_details(example_api_response)

#below based on my natlparks api tests
    # def test_retrieve_ticketMaster_info(self):
    #     example_api_response= {
    #      "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
    #     "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }]}}]}}
        
    #     #call method in views_admin.py
    #     example_api_response = get_music_data()
    #     #compare data
    #     self.assertEqual(venueName, 'U.S. Bank Stadium')



#below based on Hugh's api testing in wishful...
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
        get_music_data(params)
        mock_response =get_music_data(mock_requests_get, params) #call method in views_admin.py
        #self.assertEqual(mock_response, data)
        self.assertEqual(mock_response.performer, 'George Strait')
        self.assertEqual(mock_response.venueName, 'U.S. Bank Stadium')
        

# #was data extracted correctly from response
#     @mock.patch('requests.get', side_effect=mock_requests_get)
#     def test_extract_data_from_response(self, mock_get):
#         mock_response = {"_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
#         "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }] }} ]}}
#         self.assertEqual(performer, 'George Strait')
#         self.assertEqual(venueName, 'U.S. Bank Stadium')
        


        #below can only be used with django test case
        #response = self.client.get(reverse('artist_list') , {'search_name' : 'George Strait'} )
        
        


    # def test_retrieve_artist(self):
    #     mock_response = {
    #     "_embedded": {"events": [{"name": "George Strait", "dates": { "start": {"dateTime": "2021-07-31T22:00:00Z"}, },
    #     "_embedded": {"venues": [{"name": "U.S. Bank Stadium","city": { "name": "Minneapolis"},"state": {"stateCode": "MN", } }]}}]}}
    # #feed the mock response to the extract_music_details function
    #     data = extract_music_details(mock_response)
        
    #     self.assertEqual('George Strait', data.artist.name)


#IS THIS NEEDED?
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
        



