import requests
import os
from lmn.models import Artist,Venue,Show
from pprint import pprint
from django.http import HttpResponse
from django.db import IntegrityError
import logging


logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#running the api request and saving the data and returning an ok response
def get_all_events(request):
    data = get_event_data()
    get_and_save_event_information(data)

    return HttpResponse('ok')


# getting all the data from the api to send it elsewhere
def get_event_data():

    url = 'https://app.ticketmaster.com/discovery/v2/events' 

    api_key = os.environ.get('TICKETMASTER_KEY')

    params = {'classificaitonName' : 'music', 'city' : 'Minneapolis', 'apikey' : 'gHTG8zLgy3V0Ufmk55MGCKfhGzSMIGlM'}

    # trying to get a response from the api and returning none if it fails
    try:
        res = requests.get(url, params=params)
        data = res.json()
        return data

    except Exception as e:
        logging.error(e) #log
        return HttpResponse('could not make request')
    


# extracting the useful data from the event data we got above and saving that to the database
def get_and_save_event_information(data):


    if data != None:
        events = data['_embedded']['events']

        artist_id = None
        venue_id = None

        for event in events:

            artist_name = event['name']  # name person
            date = event['dates']['start']['localDate']  # date
            venue_name = event['_embedded']['venues'][0]['name'] # venue
            venue_city = event['_embedded']['venues'][0]['city']['name'] # city
            venue_state = event['_embedded']['venues'][0]['state']['stateCode'] #state

            #checking if event artist or venue already exists in the datbase before addding it 
            try :
                if not Artist.objects.filter(name=artist_name).exists():
                    artist = Artist(name=artist_name)
                    artist.save()

                    artist_id = artist.id #getting the id to be used in the show 
            except IntegrityError as e:
                artist = Artist.objects.get(name=artist_name)
                artist_id = artist.id
                logging.error(e)

            try:
                if not Venue.objects.filter(name=venue_name):
                    venue = Venue(name=venue_name,city=venue_city, state=venue_state)
                    venue.save()
                    
                    venue_id = venue.id
            except IntegrityError as e:
                venue = Venue.objects.get(name=venue_name)
                venue_id = artist.id
                logging.error(e)

            try:

                if artist_id != None and venue_id != None:
                    show = Show(show_date= date, artist= Artist.objects.get(pk = artist_id), venue= Venue.objects.get(pk = venue_id))
                    show.save()
            except IntegrityError as e:
                logging.error(e)

