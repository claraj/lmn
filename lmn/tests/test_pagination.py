from django.test import TestCase, client
from django.urls import reverse

class TestPagination(TestCase):
    fixtures = ['testing_users', 'testing_shows','testing_note_entries_per_page', 'testing_artist_entries_per_page',  'testing_venues']
    
    def test_number_of_note_entries_per_page(self):
        #Test that desired number of notes are present per page
        response = self.client.get(reverse('latest_notes') + '?page=1')
        context = response.context['page_obj'] # get the value from the context
        self.assertEqual(len(context), 4)# must be 15 note entries in page 1

        res = self.client.get(reverse('latest_notes') + '?page=2')
        ctx = res.context['page_obj'] # get the value from the context
        self.assertEqual(len(ctx), 1)# must be 15 note entries in page 2

    def test_number_of_venue_entries_per_page(self):
        # Test that desired number of venues are present per page
        response = self.client.get(reverse('venue_list') + '?page=1')
        context = response.context['page_obj'] # get the value from the context
        self.assertEqual(len(context), 2)# must be 2 venues entries in page 1

        res = self.client.get(reverse('venue_list') + '?page=2')
        ctx = res.context['page_obj'] # get the value from the context
        self.assertEqual(len(ctx), 1)# must be 1 venue entries in page 2

    def test_number_of_artist_entries_per_page(self):
        # Test that desired number of venues are present per page
        response = self.client.get(reverse('artist_list') + '?page=1')
        context = response.context['page_obj'] # get the value from the context
        self.assertEqual(len(context), 3)# must be 3 artist entries in page 1

        res = self.client.get(reverse('artist_list') + '?page=2')
        ctx = res.context['page_obj'] # get the value from the context
        self.assertEqual(len(ctx), 2)# must be 2 artist entries in page 2