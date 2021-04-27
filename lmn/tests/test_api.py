import requests
from django.test import TestCase
from unittest.mock import patch, call
from lmn import api_calls


class TestAPIArtist(TestCase):

    def test_artist_name_matches_result(self):
        test_artist = 'Ho99o9'
        expected_response = 'Artist: Ho99o9 From: Newark Description: None'
        test_result = api_calls.search_mb_artist_by_name(test_artist)
        self.assertEqual(expected_response, test_result)
