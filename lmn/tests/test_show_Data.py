from django.test import TestCase
from django.db import IntegrityError
from lmn.models import Venue, Artist, Show
from django.db import transaction
import logging


from lmn.views import views_admin


MODELS = [Venue,Artist,Show]

#api data for one show

mock_api_response = {"_embedded":{"events":[{"name":"Hamilton","type":"event","id":"Z7r9jZ1Ae0UeZ","test":False,"url":"http://www.ticketsnow.com/InventoryBrowse/TicketList.aspx?PID=2936080","locale":"en-us","images":[{"ratio":"4_3","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_CUSTOM.jpg","width":305,"height":225,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_EVENT_DETAIL_PAGE_16_9.jpg","width":205,"height":115,"fallback":False},{"ratio":"3_2","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RETINA_PORTRAIT_3_2.jpg","width":640,"height":427,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RECOMENDATION_16_9.jpg","width":100,"height":56,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_TABLET_LANDSCAPE_LARGE_16_9.jpg","width":2048,"height":1152,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RETINA_LANDSCAPE_16_9.jpg","width":1136,"height":639,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_TABLET_LANDSCAPE_16_9.jpg","width":1024,"height":576,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RETINA_PORTRAIT_16_9.jpg","width":640,"height":360,"fallback":False},{"ratio":"3_2","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_TABLET_LANDSCAPE_3_2.jpg","width":1024,"height":683,"fallback":False},{"ratio":"3_2","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_ARTIST_PAGE_3_2.jpg","width":305,"height":203,"fallback":False}],"sales":{"public":{"startTBD":False,"startTBA":False}},"dates":{"start":{"localDate":"2021-07-28","localTime":"19:30:00","dateTime":"2021-07-29T00:30:00Z","dateTBD":False,"dateTBA":False,"timeTBA":False,"noSpecificTime":False},"status":{"code":"rescheduled"},"spanMultipleDays":False},"classifications":[{"primary":False,"segment":{"id":"KZFzniwnSyZfZ7v7na","name":"Arts & Theatre"},"genre":{"id":"KnvZfZ7v7l1","name":"Theatre"},"subGenre":{"id":"KZazBEonSMnZfZ7vAve","name":"Musical"},"family":False}],"outlets":[{"url":"https://www.ticketmaster.com/hamilton-minneapolis-minnesota-07-28-2021/event/Z7r9jZ1Ae0UeZ","type":"tmMarketPlace"}],"seatmap":{"staticUrl":"http://resale.ticketmaster.com.au/akamai-content/maps/1254-1-1-main.gif"},"_links":{"self":{"href":"/discovery/v2/events/Z7r9jZ1Ae0UeZ?locale=en-us"},"attractions":[{"href":"/discovery/v2/attractions/K8vZ9174wRf?locale=en-us"}],"venues":[{"href":"/discovery/v2/venues/ZFr9jZedkA?locale=en-us"}]},"_embedded":{"venues":[{"name":"Orpheum Theatre - Minneapolis","type":"venue","id":"ZFr9jZedkA","test":False,"locale":"en-us","postalCode":"55403","timezone":"America/Chicago","city":{"name":"Minneapolis"},"state":{"name":"Minnesota","stateCode":"MN"},"country":{"name":"United States Of America","countryCode":"US"},"address":{"line1":"910 Hennepin Ave. S."},"location":{"longitude":"-93.286102","latitude":"44.970299"},"dmas":[{"id":336}],"upcomingEvents":{"_total":143,"tmr":97,"ticketmaster":46},"_links":{"self":{"href":"/discovery/v2/venues/ZFr9jZedkA?locale=en-us"}}}],"attractions":[{"name":"Hamilton (Touring)","type":"attraction","id":"K8vZ9174wRf","test":False,"url":"https://www.ticketmaster.com/hamilton-touring-tickets/artist/2336213","locale":"en-us","images":[{"ratio":"4_3","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_CUSTOM.jpg","width":305,"height":225,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_EVENT_DETAIL_PAGE_16_9.jpg","width":205,"height":115,"fallback":False},{"ratio":"3_2","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RETINA_PORTRAIT_3_2.jpg","width":640,"height":427,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RECOMENDATION_16_9.jpg","width":100,"height":56,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_TABLET_LANDSCAPE_LARGE_16_9.jpg","width":2048,"height":1152,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RETINA_LANDSCAPE_16_9.jpg","width":1136,"height":639,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_TABLET_LANDSCAPE_16_9.jpg","width":1024,"height":576,"fallback":False},{"ratio":"16_9","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_RETINA_PORTRAIT_16_9.jpg","width":640,"height":360,"fallback":False},{"ratio":"3_2","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_TABLET_LANDSCAPE_3_2.jpg","width":1024,"height":683,"fallback":False},{"ratio":"3_2","url":"https://s1.ticketm.net/dam/a/300/88bcb3d0-aa78-428d-ad10-52514ea72300_570131_ARTIST_PAGE_3_2.jpg","width":305,"height":203,"fallback":False}],"classifications":[{"primary":False,"segment":{"id":"KZFzniwnSyZfZ7v7na","name":"Arts & Theatre"},"genre":{"id":"KnvZfZ7v7l1","name":"Theatre"},"subGenre":{"id":"KZazBEonSMnZfZ7vAve","name":"Musical"},"type":{"id":"KZAyXgnZfZ7v7nI","name":"Undefined"},"subType":{"id":"KZFzBErXgnZfZ7v7lJ","name":"Undefined"},"family":False}],"upcomingEvents":{"_total":495,"tmr":283,"ticketmaster":212},"_links":{"self":{"href":"/discovery/v2/attractions/K8vZ9174wRf?locale=en-us"}}}]}}]},"_links":{"first":{"href":"/discovery/v2/events?city=Minneapolis&page=0&size=1"},"self":{"href":"/discovery/v2/events?size=1&city=Minneapolis"},"next":{"href":"/discovery/v2/events?city=Minneapolis&page=1&size=1"},"last":{"href":"/discovery/v2/events?city=Minneapolis&page=198&size=1"}},"page":{"size":1,"totalElements":199,"totalPages":199,"number":0}}

class TestAPIDATA(TestCase):


    # def SetUp(self):
    #     Venue.

    #testing if function saves artist show and venue data to database when called
    def test_save_artist_to_database(self):

        views_admin.get_all_events(mock_api_response)
    
        artist = Artist.objects.get(pk=1)
        self.assertEqual(artist.name, 'Hamilton')

    def test_save_venue_to_database(self):
        with transaction.atomic():

            views_admin.get_all_events(mock_api_response)
            venue = Venue.objects.get(pk=1)
            
        self.assertEqual(venue.name, 'Orpheum Theatre - Minneapolis')
        self.assertEqual(venue.state, 'MN')
        self.assertEqual(venue.city, 'Minneapolis')

    def test_save_show_to_database(self):
        
        views_admin.get_all_events(mock_api_response)

        show = Show.objects.get(pk=1)

        self.assertEqual(show.venue.name, 'Orpheum Theatre - Minneapolis')
        self.assertEqual(show.artist.name, 'Hamilton')

    ##testing if adding duplicates to the database will raise integrity errors
    def test_add_duplicate_artist(self):
        Artist(name='bob').save()

        with self.assertRaises(IntegrityError):
            Artist(name='bob').save()

    
    def test_add_duplicate_venue(self):
        Venue(name='Big stadium').save()

        with self.assertRaises(IntegrityError):
            Venue(name='Big stadium').save()

    def test_add_duplicate_show(self):
        #had to do this in a two step process otherwise the test would not pass
        venue = Venue(name='cool_stadium',city='Minneapolis', state='MN')
        venue.save()
        artist= Artist(name='bobby')
        artist.save()

        Show(show_date='2021-07-28 11:00:00',artist=artist,venue=venue).save()

        with self.assertRaises(IntegrityError):
            Show(show_date='2021-07-28 11:00:00',artist=artist,venue=venue).save()


