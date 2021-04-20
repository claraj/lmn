import requests
from .models import Artist, Venue


def search_mb_place(place):
    """ searches musicbrainz API for a venue and returns a list of matches some results will not have an address
    so there is a try/except to handle for now """
    url = f'http://musicbrainz.org/ws/2/place/?query=place:{place}'
    headers = {"User-Agent": "LMNApp/1.0(sean@dropanddram.com)", "Accept": "application/json"}
    params = {
        'fmt=': 'json',
        'limit': 10
    }
    data = requests.get(url, headers=headers, params=params).json()
    places = data['places']
    result_list = []
    for place in places:
        new_name = place['name']

        new_address = place.get('address')
        new_venue = Venue(new_name, new_address)
        result_list.append(new_venue)
    return result_list


def search_mb_artist_by_name(name):
    """ searches musicbrainz API for an artist and returns a list of matches some results will not have a place of
    origin or a description so there are try/excepts to handle for now """
    url = f'http://musicbrainz.org/ws/2/artist/?query=artist:{name}'
    headers = {"User-Agent": "LMNApp/1.0(sean@dropanddram.com)", "Accept": "application/json"}
    params = {
        'fmt': 'json',
        'limit': 10
    }
    data = requests.get(url, headers=headers, params=params).json()
    artists = data['artists']
    result_list = []
    for artist in artists:
        new_name = artist['name']
        try:
            new_hometown = artist['begin-area']['name']
        except KeyError as e:
            new_hometown = 'Unknown Origins'
            print(f'Error, no hometown {e}')
        try:
            new_desc = artist['disambiguation']
        except KeyError as e:
            new_desc = 'None'
            print(f'Error, no description available {e}')

        new_artist = Artist(new_name, new_hometown, new_desc)
        result_list.append(new_artist)
    for a in result_list:
        if a.description == 'None':
            result_list.remove(a)
    return result_list
