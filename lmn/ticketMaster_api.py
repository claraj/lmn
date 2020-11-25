import requests
from pprint import pprint

def get_all_events():

    url = 'https://app.ticketmaster.com/discovery/v2/events.json?apikey=gHTG8zLgy3V0Ufmk55MGCKfhGzSMIGlM&classificaitonName=music&stateCode=MN'


    data = requests.get(url).json()

    print(data['_embedded']['events'][3]['name'])  # name person
    print(data['_embedded']['events'][3]['dates']['start']['localDate'])  # date
    print(data['_embedded']['events'][3]['_embedded']['venues'][0]['name']) # venue
    #todo name show

# def get_venue():
#     #not needed anymore
    
# def get_artist():
#     not needed anymore



get_all_events()