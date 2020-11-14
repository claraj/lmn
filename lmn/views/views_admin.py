import os
import requests
import re
from ..models import Artist, Venue, Show
from django.http import HttpResponse

#getting data from  ticketmaster api
key = os.environ.get('TICKETMASTER_KEY')
url = 'https://app.ticketmaster.com/discovery/v2/events'
classificationName = 'music'
city = 'Minneapolis'


def get_music_data(request):
    try:
        query= {'classificationName': classificationName, 'city' : city, 'apikey': key}
        response = requests.get(url, params=query)
        response.raise_for_status()  #will raise an exception for 400(client) or 500(server) errors
        data = response.json() 
        print(data)
        events = data['_embedded']['events']
        for event in events: 
            pattern = '[A-Za-z\s]{1,30}' #do I need r?
            performerLong = event['name']
            performerObj = re.search(pattern, performerLong)
            performer = performerObj.group()
            venueName = event['_embedded']['venues'][0]['name']
            venueCity = event['_embedded']['venues'][0]['city']['name']
            venueState = event['_embedded']['venues'][0]['state']['stateCode']
            show_date = event['dates']['start']['localDate']
            #perhaps problem here; my constraint is on Show
            Artist(name=performer).save() #linking info to models and saving it
            Venue(name=venueName, city=venueCity, state=venueState).save()
            Show(data=show_date).save()
            return HttpResponse('ok')
        
    except Exception as ex:
        print(ex)
       # logging.exception(ex)



