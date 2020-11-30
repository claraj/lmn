import requests
import os
from ..models import Artist,Show,Venue
from pprint import pprint


def get_all_events():
    data = get_event_data()
    get_and_save_event_information(data)



def get_event_data():

    url = 'https://app.ticketmaster.com/discovery/v2/events'

    params = {'classificaitonName' : 'music', 'city' : 'Minneapolis', 'apikey' : 'gHTG8zLgy3V0Ufmk55MGCKfhGzSMIGlM'}

    try:
        res = requests.get(url, params=params)
        data = res.json()
        return data

    except Exception as e:
        print(e)
        return None
    



def get_and_save_event_information(data):


    events = data['_embedded']['events']
    information_list = []


    for event in events:

        print(event['name'])  # name person
        print(event['dates']['start']['localDate'])  # date
        print(event['_embedded']['venues'][0]['name']) # venue
        print(event['_embedded']['venues'][0]['city']['name']) # city
        print(event['_embedded']['venues'][0]['state']['stateCode']) #state



get_all_events()