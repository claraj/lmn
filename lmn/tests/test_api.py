import requests
from django.test import TestCase
from unittest.mock import patch, call
from lmn import api_calls


class TestAPIArtist(TestCase):

    def test_artist_name_matches_result(self):
        test_artist = 'Ho99o9'
        expected_response = 'Artist: Ho99o9 From: Newark Description: None'
        test_result = api_calls.search_mb_artist_by_name(test_artist)[0]
        self.assertEqual(expected_response, str(test_result))

    def test_artist_name_not_matching_if_not_equal(self):
        test_artist = 'Horror'
        expected_response = 'Artist: Ho99o9 From: Newark Description: None'
        test_result = api_calls.search_mb_artist_by_name(test_artist)[0]
        self.assertNotEqual(expected_response, str(test_result))

    def test_empty_search_string_produces_no_results(self):
        test_artist = ''
        expected_response = 0
        test_result = api_calls.search_mb_artist_by_name(test_artist)
        self.assertEqual(expected_response, len(test_result))

    def test_blank_search_string_produces_no_results(self):
        test_artist = '      '
        expected_response = 0
        test_result = api_calls.search_mb_artist_by_name(test_artist)
        self.assertEqual(expected_response, len(test_result))


class TestAPIVenue(TestCase):
    def test_venue_name_matches_result(self):
        test_venue = 'middle east'
        expected_response = 'Name: The Middle East Location: 472-480 Massachusetts Avenue, Central Square, Cambridge, ' \
                            'MA 02139'
        test_result = api_calls.search_mb_place(test_venue)[0]
        self.assertEqual(expected_response, str(test_result))

    def test_venue_name_not_matching_if_not_equal(self):
        test_venue = '1st ave'  # 'first ave or first avenue will result in the correct venue being #1
        expected_response = '701 First Avenue North, Minneapolis, MN 55403'
        test_result = api_calls.search_mb_place(test_venue)[0]
        self.assertNotEqual(expected_response, str(test_result))

    def test_empty_search_string_produces_no_results(self):
        test_venue = ''
        expected_response = 0
        test_result = api_calls.search_mb_place(test_venue)
        self.assertEqual(expected_response, len(test_result))

    def test_blank_search_string_produces_no_results(self):
        test_venue = ''
        expected_response = 0
        test_result = api_calls.search_mb_place(test_venue)
        self.assertEqual(expected_response, len(test_result))
