from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User

from unittest.mock import patch, create_autospec, MagicMock
from ..twitter import authorize, make_tweet_text, post_tweet, tweet_note
import tweepy
from tweepy.error import TweepError


# These are gonna be hard to explain.
    # They did not end up being that hard to explain

class TestAuthAndNote(TestCase):
    fixtures = [ 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes' ]

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    # the authorize test is simple because those tweepy functions are
    # all just setting up an api object, so we just have to check that
    # the object got made properly. (it only has the search_host value
    # if it's made it through all 3 steps)
    def test_auth_respond_with_usable_api_object(self):
        auth_response = authorize()
        self.assertNotEqual(auth_response, 'error')
        self.assertEqual(auth_response.search_host, 'search.twitter.com')


    # This checks that a note successfully goes in and comes out like the
    # text. simple enough, since it should just pull the show details and
    # such. 
    def test_create_note_no_truncation(self):
        note_ok = Note.objects.filter(pk=4).first()
        note_check = 'REM at The Turf Club.\ntitle: text -alice'
        test_note = make_tweet_text(note_ok)
        self.assertEqual(note_check, test_note)


    # this is goofy.
    # It needs a massive text input to break the 280 character limit! 
    # after that, those notes are saved and can be checked against each other.
    # the edited string should end early and have the last three characters replaced
    def test_create_note_with_truncation(self):
        big_string = 248 * str('0')
        note_check = (f"REM at The Turf Club.\ntitle: {big_string}...")

        big_string = 265 * str('0')
        note_long = Note.objects.filter(pk=4).first()
        note_long.text = big_string
        
        test_note = make_tweet_text(note_long)
        self.assertEqual(note_check, test_note)

# Here's where stuff gets weird. 

class TestTweetFailure(TestCase):
    fixtures = [ 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes' ]       

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    # https://stackoverflow.com/questions/37039512/mocking-twitters-api-library-with-pythons-patch-decorator
    # Reading up on how this all works. I think I understand it, and I absolutely understand why they
    # call it magicmock...
    # create_autospec is creating our api object that tweepy needs for authorization and to have
    # the update status function.
    # That update_status function is then replaced with MagicMock's return for 'error'
    # pretending that the tweet failed to send.
    # I don't totally understand mocking tweepy.API, mocking the API itself? unsure.
        # Addendum: TOTALLY NECESSARY. Without mocking tweepy.API, the test will 
        # *actually make the tweet* so it's needed to step in and stop that.
    # then the usual new note reverse is run, so the test pretends it's making a new note
    # this time including the post_type as Tweet, so it attempts to make a tweet!
    # MagicMock steps in and responds with 'error', causing the error message to get displayed
    def test_tweet_failure(self):
        api = create_autospec(tweepy.API, name='testAPI')
        api.update_status = MagicMock(return_value='error')
        tweepy.API = MagicMock(return_value=api)

        new_note_url = reverse('new_note', kwargs={'show_pk':1})
        response = self.client.post(new_note_url, { 'text':'check', 'title':'double', 'post_type':'Tweet and Add Note'}, follow=True)
        self.assertContains(response, 'Please try again later.')

# MagicMock wouldn't reset between functions? so new testcase!

class TestTweetSuccess(TestCase):
    fixtures = [ 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes' ]       

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    # This time, update_status will get a 'success' return, meaning it succeeded in tweeting, and the page contains the right message.
    def test_tweet_success(self):
        api = create_autospec(tweepy.API, name='testAPI')
        api.update_status = MagicMock(return_value='success')
        tweepy.API = MagicMock(return_value=api)

        new_note_url = reverse('new_note', kwargs={'show_pk':1})
        response = self.client.post(new_note_url, { 'text':'um', 'title':'yea?', 'post_type':'Tweet and Add Note'}, follow=True)
        self.assertContains(response, 'Successfully Tweeted')

