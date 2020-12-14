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

    """This function calls two other functions, and serves to pass data between them, then returns a response depending on if we successfuly exctracted the data or not

    :return: returning an http response depending on wether we got data from the api or not
    :rtype: HttpResponse
    """

    data = get_event_data()

    if(data != None):

        get_and_save_event_information(data)
        return HttpResponse('ok')

    else:
        return HttpResponse('404 - could not access API')


# getting all the data from the api to send it elsewhere
def get_event_data():
    """This function makes a request to the ticketmaster api, and then returns all the raw json data

    :return: either we return a dictionary with all the json data, or a HttpResponse with an error code
    :rtype: Dictionary
    """

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
        return None
    


# extracting the useful data from the event data we got above and saving that to the database
def get_and_save_event_information(data):
    """This funtion takes all the data that was aquried from the api, parses throguh it getting the useful info, and stores that into our database.

    :param data: Json data we got from the database
    :type data: Dictionary
    
    """

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


