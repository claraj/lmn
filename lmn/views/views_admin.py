import os
import requests
import re
from ..models import Artist, Venue, Show
from django.http import HttpResponse
from django.http import Http404

#getting data from  ticketmaster api
key = os.environ.get('TICKETMASTER_KEY')
url = 'https://app.ticketmaster.com/discovery/v2/events'
classificationName = 'music'
city = 'Minneapolis'

def get_music_data(request):
   #data=get_music_data_from_ticketMaster(request)
    #extract_music_details(data)

#def get_music_data_from_ticketMaster(request):
    try:
        query= {'classificationName': classificationName, 'city' : city, 'apikey': key}
        response = requests.get(url, params=query)
        response.raise_for_status()  #will raise an exception for 400(client) or 500(server) errors
        data = response.json() 
        #return data
    
#def extract_music_details(data):
        events = data['_embedded']['events']
        
        for event in events: 
            pattern = '[A-Za-z\s]{1,30}' 
            performerLong = event['name']
            performerObj = re.search(pattern, performerLong)
            performer = performerObj.group()
            venueName = event['_embedded']['venues'][0]['name']
            venueCity = event['_embedded']['venues'][0]['city']['name']
            venueState = event['_embedded']['venues'][0]['state']['stateCode']
            
            show_date_time = event['dates']['start']['dateTime']   
            
            ##linking info to models and saving it
            try: #if this artist already in database, don't add it again
                artist = Artist.objects.get(name=performer)
            except:# otherwise add a new artist 
                artist = Artist(name=performer)
                artist.save() #must save the new artist, then get id
                artist.id
            try:
                venue=Venue.objects.get(name=venueName)
            except:
                venue = Venue(name=venueName, city=venueCity, state=venueState)
                venue.save()
                venue.id
            try: #if this show already in dbase, don't add it again
                show = Show.objects.get(show_date=show_date_time, artist_id = artist.id, venue_id = venue.id)
            except: #otherwise, make a new Show object and save it
                show=Show(show_date=show_date_time, artist_id = artist.id, venue_id = venue.id)
                show.save()
        return HttpResponse('ok')
            
    except Exception as ex:
        print(ex)
       # logging.exception(ex)



