from django.contrib import messages
import tweepy
import os
import requests
import logging

consumer_key = os.getenv('T_API_KEY')
consumer_secret = os.getenv('T_API_KEY_SEC')
access_token = os.getenv('T_ACCESS_TOK')
access_secret = os.getenv('T_ACCESS_TOK_SEC')


def tweet_note(request, note):
    api = authorize()
    if api == 'error':
        messages.error(request, 'The site was unable to authorize to the Twitter account!')
    else:
        response = post_tweet(api, note)
        if response == 'error':
            messages.error(request, 'The site was unable to tweet the note!')
        elif response == 'length error':
            messages.error(request, 'The note was posted, but was too long to tweet')
        else:
            messages.success(request, 'Successfully Tweeted your note to our site account!')


def authorize():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        return api
    except tweepy.TweepError as err:
        err_message = err.args[0][0]['message']
        err_code = err.args[0][0]['code']
        logging.error(f'tweet failed due to error code {err_code}: {err_message}')
        return 'error'


def post_tweet(api, note):

    if len(str(note)) <= 240:
        try:
            response = api.update_status(f'{note.show.artist.name} at {note.show.venue.name}.\n{note.title}: {note.text} -{note.user}')
            return response
        except tweepy.TweepError as err:
            err_message = err.args[0][0]['message']
            err_code = err.args[0][0]['code']
            logging.error(f'tweet failed due to error code {err_code}: {err_message}')
            return 'error'
    else:
        return 'length error'