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
    try:
        data = requests.get(url, headers=headers, params=params).json()  # JSON response from API
        places = data['places']  # gets all of the place values
        result_list = []
        for place in places:
            new_name = place['name']
            if new_name is not None:  # weeds out any venues without names
                new_address = place.get('address')
                if new_address is not None:  # weeds out any venues without addresses
                    new_venue = Venue(name=new_name, address=new_address)  # if the venues have info, creates a venue
                    result_list.append(new_venue)  # and adds it to the result list
        return result_list
    except requests.ConnectionError as e:
        print(f'Error with connection {e}')
        return None


def search_mb_artist_by_name(name):
    """ searches musicbrainz API for an artist and returns a list of matches some results will not have a place of
    origin or a description so there are try/excepts to handle for now """
    url = f'http://musicbrainz.org/ws/2/artist/?query=artist:{name}'
    headers = {"User-Agent": "LMNApp/1.0(sean@dropanddram.com)", "Accept": "application/json"}
    params = {
        'fmt': 'json',
        'limit': 10
    }
    try:
        data = requests.get(url, headers=headers, params=params).json()
        artists = data['artists']
        print(len(data))
        result_list = []
        for artist in artists:
            new_name = artist['name']
            try:
                new_hometown = artist['begin-area']['name']
            except KeyError as e:
                new_hometown = 'Unknown Origins'  # if no city of origin provided
                print(f'Error, no hometown {e}')
            try:
                new_desc = artist['disambiguation']  # API description of artist
            except KeyError as e:
                new_desc = None
                print(f'Error, no description available {e}')
            new_artist = Artist(name=new_name, hometown=new_hometown, description=new_desc)
            result_list.append(new_artist)
            for a in result_list:
                if a.description is None:  # currently removing any Artists without description
                    result_list.remove(a)
        return result_list  # if successful, returns a list of artist objects
    except requests.ConnectionError as e:  # if no response from API returns none
        print(f'Error with connection {e}')
    return None
