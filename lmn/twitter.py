from django.contrib import messages
import tweepy
import os
import requests
import logging

# consumer keys required for twitter app access, access tokens required for *account* access
consumer_key = os.getenv('T_API_KEY')
consumer_secret = os.getenv('T_API_KEY_SEC')
access_token = os.getenv('T_ACCESS_TOK')
access_secret = os.getenv('T_ACCESS_TOK_SEC')



def tweet_note(request, note):
    # the note used for the tweet needs to be in a different format
    # so it's adapted into a more usable string, this can also truncate it
    # if the string text is too long (taking into account all show info, 
    # title, and text)
    adapted_note = make_tweet_text(note)

    # from here, the authorization has to be run, this doesn't yet contact 
    # the API! Explained further in that function.
    api = authorize()

    # After the note is ready, the api object has the keys set in, it can go to the
    # API itself and post the tweet! The response from that can be an error
    # if a tweepy error is raised
    response = post_tweet(api, adapted_note)
    if response == 'error':
        messages.error(request, 'We weren\'t able to tweet your note this time! Please try again later.')
    else:
        messages.success(request, 'Successfully Tweeted your note to our site account!')


def make_tweet_text(note):
    # Simple function, this takes the note object and splits it into a more tweet-able format
    # since we sort of only care a bit about the show, then just text and title from the user
    # If that note is over 280, it's truncated so it still fits in the 280 character limit!
    adapted_note = f'{note.show.artist.name} at {note.show.venue.name}.\n{note.title}: {note.text} -{note.user}'

    if len(adapted_note) > 280:
        sliced_note = adapted_note[0:277]
        truncated = sliced_note + '...'
        return truncated

    return adapted_note


def authorize():
    # Mentioned earlier, this function does not actually contact the API,
    # these tweepy functions create the necessary *object* that will be passed
    # to the API later. This means it will eventually contain the
    # keys, tokens, and note before tweepy sends it to the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api


def post_tweet(api, note):
    # This is where the API is actually contacted. Using the update_status function
    # the note is sent through tweepy to the Twitter API and the tweet is posted.
    # Or if it breaks and raises a tweepy error (like if you're offline, )
    try:
        response = api.update_status(note)
        return response
    except tweepy.TweepError as err:
        logging.error(f'tweet failed due to error code {err}')
        return 'error'

