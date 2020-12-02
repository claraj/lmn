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

# function takes the request to direct the messages, and note for tweeting
def tweet_note(request, note):
    # initially requires authorization!
    api = authorize()
    # if that authorization fails (various tweepy error possible, which are logged)
    # then the message is sent and the new_note function continues uninterrupted
    if api == 'error':
        messages.error(request, 'The site was unable to authorize to the Twitter account!')
    # if it didn't return error, then it should have the ok from tweepy
    else:
        # then it will attempt to tweet the note, which requires the auth and note
        response = post_tweet(api, note)
        # that returns a response based on any tweepy errors raised or if there were none
        # these messages are then sent to the note_detail page to display at the top
        if response == 'error':
            messages.error(request, 'The site was unable to tweet the note!')
        elif response == 'length error':
            messages.error(request, 'The note was posted, but was too long to tweet')
        else:
            messages.success(request, 'Successfully Tweeted your note to our site account!')


def authorize():
    try:
        # to authorize, it uses tweepy's OAuthHandler, which returns an auth object created using the key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # within that object, the access token and secret are set using the env variable keys
        auth.set_access_token(access_token, access_secret)
        # then that's passed through tweepy to the API to get a return from twitter.
        api = tweepy.API(auth)
        return api
    # tweepy errors that are raised and logged and error is returned to the main
    # which results in a more user friendly response
    except tweepy.TweepError as err:
        err_message = err.args[0][0]['message']
        err_code = err.args[0][0]['code']
        logging.error(f'tweet failed due to error code {err_code}: {err_message}')
        return 'error'


def post_tweet(api, note):
    # the note is adapted to a twitter-friendly version
    adapted_note = f'{note.show.artist.name} at {note.show.venue.name}.\n{note.title}: {note.text} -{note.user}'
    # then before attempting to use the API, the length is checked
    if len(adapted_note) <= 240:
        try:
            # this runs the update status function of the API bit returned by tweepy earlier, passing the adapted note to it
            response = api.update_status(adapted_note)
            # might not be necessary? so long as it doesn't return error, it's ok and the tweet is posted
            return response
        # if tweepy raises an error, that's logged and the user sees a more friendly error
        except tweepy.TweepError as err:
            err_message = err.args[0][0]['message']
            err_code = err.args[0][0]['code']
            logging.error(f'tweet failed due to error code {err_code}: {err_message}')
            return 'error'
    else:
        return 'length error'