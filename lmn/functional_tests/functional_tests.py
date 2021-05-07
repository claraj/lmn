
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


class HomePageTest(LiveServerTestCase):
    """ Hello Selenium """

    def setUp(self):
        self.browser = webdriver.Chrome()
        

    def tearDown(self):
        self.browser.quit()
        

    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('LMN', self.browser.title)
        self.assertIn('Welcome to Live Music Notes', self.browser.page_source)
        

class BrowseArtistsTests(LiveServerTestCase):

    fixtures = [
        'fn_testing_users', 
        'fn_testing_artists', 
        'fn_testing_venues', 
        'fn_testing_shows', 
        'fn_testing_notes'
    ]

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 2)


    def tearDown(self):
        self.browser.quit()
    

    def test_browsing_artists(self):

        # Start on home page
        self.browser.get(self.live_server_url)

        # Find and click on artists link
        artist_list_link = self.browser.find_element_by_link_text('Artists')
        artist_list_link.click()

        artists = ['ACDC', 'REM', 'Yes']

        artist_divs = self.browser.find_elements_by_class_name('artist')

        for artist, div in zip(artists, artist_divs):
            # assert artist name is present
            self.assertIn(artist, div.text)

            # find a link is present with artist name - exception raised if not found
            div.find_element_by_link_text(artist)
            # Find the link to view that artist's shows (which will lead to notes).
            #  Again, exception raised if not present onn page
            div.find_element_by_link_text(f'{artist} notes')


        # Are we on the right page? Do this after finding elements so know page has loaded
        self.assertIn('/artists/list/', self.browser.current_url)
        self.assertIn('Artist List', self.browser.page_source)  
        # Could also put the title in a div or header element, and find that, and verify correct text.

        # Get a link to one of the artists
        rem_link = self.browser.find_element_by_link_text('REM')
        # click this link
        time.sleep(1)  # wait for link to be ready, really ready. FIXME 
        rem_link.click()
        
        # Assert that artist's info is shown on new page
        # Assert that the URL is as expected. REM pk = 1.

        artist_name = self.wait.until(
            EC.presence_of_element_located((By.ID, 'artist-name'))
        )

        self.assertIn('REM', artist_name.text)
        self.assertIn('/artists/detail/1', self.browser.current_url)

        # go back to artists list
        self.browser.back()

        # Get a link to that artist's shows (and to notes)
        rem_notes = self.browser.find_element_by_link_text('REM notes')
        # Click on shows/notes link
        rem_notes.click()

        title = self.browser.find_element_by_id('venues-for-artist-title')
        # On correct page? Verify title, and URL

        self.assertIn('Venues that REM has played at', title.text)
        self.assertIn('artists/venues_played/1', self.browser.current_url)

        # assert list of venues that artist has played at is shown, most recent first
        # Should be show pk = 2 venue 1 first ave on 2017-01-02 , show pk = 1 venue 2, turf club on 2016-11-02
        # Assert a link to add notes is shown for each show
        expected_shows = [ 
            {'pk': 2, 'show_date': 'Jan. 2, 2017', 'venue': 'The Turf Club'},
            {'pk': 1, 'show_date': 'Nov. 4, 2016', 'venue': 'First Avenue'} 
        ]

        show_divs = self.browser.find_elements_by_class_name('show')

        for show, div in zip(expected_shows, show_divs):
            self.assertIn(show['venue'], div.text)
            self.assertIn(show['show_date'], div.text)

        # click on one of the shows - get the first match (Turf Club, Jan 2)
        see_notes_add_own = self.browser.find_element_by_partial_link_text('See notes for this')
        time.sleep(1)  # FIXME wait correctly
        see_notes_add_own.click()

        # verify list of notes for that show are shown
        # verify on correct page
        title = self.browser.find_element_by_id('show-title')
        self.assertIn('Notes for REM at The Turf Club on Jan. 2, 2017', title.text)
        self.assertIn('notes/for_show/2', self.browser.current_url)

        # should be two notes, awsome and ok, in that order - most recently posted first
        # Trying out a different way of finding and checking properties of elements. A loop is less typing:)

        first_note_div = self.browser.find_element_by_id('note_2')
        # Is the title (in a H3 element) 'awesome' ?
        self.assertIn('awesome', first_note_div.find_element_by_tag_name('h3').text)
        # Check note text
        self.assertIn('yay!', first_note_div.text)
        # By correct user?
        self.assertIn('bob', first_note_div.find_element_by_class_name('user').text)
        # Posted on the epected day?
        self.assertIn('Posted on Feb. 13, 2017', first_note_div.text)

        # Repeat for second note
        second_note_div = self.browser.find_element_by_id('note_1')
        self.assertIn('ok', second_note_div.find_element_by_tag_name('h3').text)
        self.assertIn('alright', second_note_div.text)
        self.assertIn('alice', second_note_div.find_element_by_class_name('user').text)
        # Posted on the expected day?
        self.assertIn('Posted on Feb. 12, 2017', second_note_div.text)



    def test_searching_artists(self):
        self.browser.get(self.live_server_url + '/artists/list')

        # Verify title
        title = self.browser.find_element_by_id('artist-list-title')
        self.assertIn('All artists', title.text)

        # Find search form. Django gives each form input an id.
        search_input = self.browser.find_element_by_id('id_search_name')

        # ** Exact match search **

        # Enter text and submit form
        search_input.send_keys('Yes')  # one exact match
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (yuck). TODO how to check for search page load?

        # Verify correct title
        title = self.browser.find_element_by_id('artist-list-title')
        self.assertIn('Artists matching \'Yes\'', title.text)

        # Exactly one result for Yes
        self.assertIn('Yes', self.browser.page_source)
        self.assertNotIn('REM', self.browser.page_source)
        self.assertNotIn('ACDC', self.browser.page_source)

        # ** partial text search **
        search_input = self.browser.find_element_by_id('id_search_name')

        # Enter text and submit form
        search_input.send_keys('e')  # should return two partial-text matches; search is case-insensitive
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. FIXME

        # Verify correct title
        title = self.browser.find_element_by_id('artist-list-title')
        self.assertIn('Artists matching \'e\'', title.text)

        self.assertIn('Yes', self.browser.page_source)
        self.assertIn('REM', self.browser.page_source)
        self.assertNotIn('ACDC', self.browser.page_source)

        # **  No matches **
        search_input = self.browser.find_element_by_id('id_search_name')

        # Enter text and submit form
        search_input.send_keys('ZZZ ZZZ')  # no exact matches
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (meh).

        # Verify correct title
        title = self.browser.find_element_by_id('artist-list-title')  # id with spaces, ??
        self.assertIn('Artists matching \'ZZZ ZZZ\'', title.text)

        self.assertNotIn('Yes', self.browser.page_source)
        self.assertNotIn('REM', self.browser.page_source)
        self.assertNotIn('ACDC', self.browser.page_source)

        # 'No artists found message'

        self.assertIn('No artists found', self.browser.page_source)

        # Find and click 'clear' button

        clear = self.browser.find_element_by_partial_link_text('clear')
        clear.click()

        time.sleep(1)  # Wait for page to load. (still FIXME

        # After search cleared, verify all artists are shown

        self.assertIn('Yes', self.browser.page_source)
        self.assertIn('REM', self.browser.page_source)
        self.assertIn('ACDC', self.browser.page_source)


class BrowseVenuesTests(LiveServerTestCase):

    fixtures = [
        'fn_testing_users', 
        'fn_testing_artists', 
        'fn_testing_venues', 
        'fn_testing_shows', 
        'fn_testing_notes'
    ]

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()
    

    def test_browsing_venues(self):
        # Start on home page
        self.browser.get(self.live_server_url)

        # Find and click on venues link
        venue_list_link = self.browser.find_element_by_link_text('Venues')
        venue_list_link.click()

        venues = ['First Avenue', 'Target Center', 'The Turf Club']

        venue_divs = self.browser.find_elements_by_class_name('venue')

        for venue, div in zip(venues, venue_divs):
            self.assertIn(venue, div.text)   # Venue name present
            # find a link is present with venue name - exception raised if not found
            div.find_element_by_link_text(venue)
            # Find the link to view that venue's shows (which will lead to notes). 
            # Again, exception raised if not found
            div.find_element_by_link_text('%s notes' % venue)

        # Are we on the right page? Do this after finding elements so know page has loaded
        self.assertIn('/venues/list/', self.browser.current_url)
        self.assertIn('Venue List', self.browser.page_source)  
        # Could also put the title in a div or header element with a HTML id,
        # and find that element, and verify it contains the correct text.

        # Get a link to one of the venues
        fa = self.browser.find_element_by_link_text('First Avenue')

        # click the link to First Avenue
        fa.click()

        # Venue information shown on page
        self.assertIn('First Avenue', self.browser.find_element_by_id('venue-name').text)
        self.assertIn('Minneapolis', self.browser.find_element_by_id('venue-city').text)
        self.assertIn('MN', self.browser.find_element_by_id('venue-state').text)

        self.assertIn('/venues/detail/1', self.browser.current_url)

        # go back
        self.browser.back()

        # Get a link to that venue's shows (and to notes)
        fa_notes = self.browser.find_element_by_link_text('First Avenue notes')

        # Click on shows/notes link
        fa_notes.click()

        title = self.browser.find_element_by_id('artists-at-venue-title')
        # On correct page? Verify title, and URL
        self.assertIn('Artists that have played at First Avenue', title.text)
        self.assertIn('venues/artists_at/1', self.browser.current_url)

        # assert a list of venues that venue has played at is shown, most recent first
        # Should be 
        #  show pk=2, venue=1, First ave on 2017-01-02,
        #  show pk=1 venue=2, turf club on 2016-11-02
        # assert a link to add notes is shown for each show
        expected_shows = [
            {'pk': 4, 'show_date': 'Jan. 21, 2017', 'artist': 'ACDC'},
            {'pk': 1, 'show_date': 'Nov. 4, 2016', 'artist': 'REM'}
        ]

        show_divs = self.browser.find_elements_by_class_name('show')

        for show, div in zip(expected_shows, show_divs):
            self.assertIn(show['artist'], div.text)
            self.assertIn(show['show_date'], div.text)

        # click on one of the shows - get the first match (ACDC, Jan 21)
        see_notes_add_own = self.browser.find_element_by_partial_link_text('See notes for this')
        
        time.sleep(1)  # FIXME
        see_notes_add_own.click()

        # verify list of notes for that show are shown
        # verify on correct page
        title = self.browser.find_element_by_id('show-title')
        self.assertIn('Notes for ACDC at First Avenue on Jan. 21, 2017', title.text)
        self.assertIn('notes/for_show/4', self.browser.current_url)

        # should be one note.

        first_note_div = self.browser.find_element_by_id('note_4')
        # Is the title (in a H3 element) 'mythical' ?
        self.assertIn('mythical', first_note_div.find_element_by_class_name('note-title').text)
        # Check note text
        self.assertIn('boo', first_note_div.find_element_by_class_name('note-text').text)
        # By correct user?
        self.assertIn('cat', first_note_div.find_element_by_class_name('user').text)
        # Posted on the expected day?
        self.assertIn('Posted on Feb. 15, 2017', first_note_div.find_element_by_class_name('note-info').text)

        # verify link button to add user's own notes for that show is displayed
        # if it's not there, this line will error
        self.browser.find_element_by_link_text('Add your own notes for this show')
        
        # Adding a note requires authentication - will do this in another test.

        # Test artist with no shows
        self.browser.back()  # back to list of shows
        self.browser.back()  # and back to list of artists

        no_shows_venue = self.browser.find_element_by_link_text('Target Center notes')
        no_shows_venue.click()

        # This page should say 'we have no records of shows at this venue'
        no_show_para = self.browser.find_element_by_id('no-results')
        self.assertIn('no records of shows', no_show_para.text)


    def test_searching_venues(self):
        self.browser.get(self.live_server_url + '/venues/list')

        # Verify title
        title = self.browser.find_element_by_id('venue-list-title')
        self.assertIn('All venues', title.text)

        # Find search form. Django gives each form input an id.
        search_input = self.browser.find_element_by_id('id_search_name')

        # ** Exact match search **

        # Enter text and submit form
        search_input.send_keys('First Avenue')  # one exact match
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        # Wait for page to load. (yuck). 
        # FIXME better way to check for search page load? 
        # Can't search for an element to force Selenium to wait because it's the same page.
        time.sleep(1)  

        # Verify correct title
        title = self.browser.find_element_by_id('venue-list-title')
        self.assertIn('Venues matching \'First Avenue\'', title.text)

        # Exactly one result for First Avenue
        self.assertIn('First Avenue', self.browser.page_source)
        self.assertNotIn('Target Center', self.browser.page_source)
        self.assertNotIn('The Turf Club', self.browser.page_source)

        # Check for no 'No venues found' message
        self.assertNotIn('No venues found', self.browser.page_source)

        # ** partial text search **

        search_input = self.browser.find_element_by_id('id_search_name')

        # Enter text and submit form
        search_input.send_keys('a')  # should return two partial-text matches; search is case-insensitive
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (ugh).

        # Verify correct title
        title = self.browser.find_element_by_id('venue-list-title')
        self.assertIn('Venues matching \'a\'', title.text)

        self.assertIn('First Avenue', self.browser.page_source)
        self.assertIn('Target Center', self.browser.page_source)
        self.assertNotIn('The Turf Club', self.browser.page_source)
        # Check for no 'No venues found' message
        self.assertNotIn('No venues found', self.browser.page_source)

        # **  No matches **
        search_input = self.browser.find_element_by_id('id_search_name')

        # Enter text and submit form
        search_input.send_keys('ZZZ ZZZ')  # no exact matches
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (meh).

        # Verify correct title
        title = self.browser.find_element_by_id('venue-list-title')  # id with spaces, ??
        self.assertIn('Venues matching \'ZZZ ZZZ\'', title.text)

        self.assertNotIn('First Avenue', self.browser.page_source)
        self.assertNotIn('Target Center', self.browser.page_source)
        self.assertNotIn('The Turf Club', self.browser.page_source)

        # Check for 'No venues found' message
        self.assertIn('No venues found', self.browser.page_source)

        # Find and click 'clear' button

        clear = self.browser.find_element_by_partial_link_text('clear')
        clear.click()

        time.sleep(1)  # Wait for page to load. (still yuck).

        # After search cleared, verify all venues are shown

        self.assertIn('First Avenue', self.browser.page_source)
        self.assertIn('Target Center', self.browser.page_source)
        self.assertIn('The Turf Club', self.browser.page_source)


class NotesTests(LiveServerTestCase):

    fixtures = [
        'fn_testing_users', 
        'fn_testing_artists', 
        'fn_testing_venues', 
        'fn_testing_shows', 
        'fn_testing_notes'
    ]


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def test_add_note_for_show_when_logged_in(self):
        # Log in
        self.browser.get(self.live_server_url + '/accounts/login')
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('bob')
        password.send_keys('qwertyuiop')
        username.submit()

        time.sleep(1)

        # Get show page, the list of notes for an example show
        self.browser.get(self.live_server_url + '/notes/for_show/2')

        time.sleep(1)  

        # Find and click on 'add note' button
        add_note_link = self.browser.find_element_by_id('add-new-show-link')
        add_note_link.click()

        time.sleep(1)    # FIXME

        # Should be on the Add Note page

        # Find form elements
        title_area = self.browser.find_element_by_id('id_title')
        text_area = self.browser.find_element_by_id('id_text')

        # Check URL (after finding elements, so will know page has loaded)
        self.assertIn('notes/add/2', self.browser.current_url)

        title_area.send_keys('Fab')
        text_area.send_keys('Best ever')
        title_area.submit()  # Convenience method for submitting form with this element in

        # Should now be on note detail page. Title will be 'band at venue by user'
        time.sleep(1)    # FIXME
        
        title = self.browser.find_element_by_id('note-page-title')
        self.assertIn('REM at The Turf Club by bob', title.text)

        note_title = self.browser.find_element_by_id('note-title')
        self.assertIn('Fab', note_title.text)

        note_text = self.browser.find_element_by_id('note-text')
        self.assertIn('Best ever', note_text.text)

        # Correct URL?
        self.assertIn('/notes/detail/5', self.browser.current_url)



    def test_add_note_redirect_to_login_and_back_to_add_note(self):

        # At the beginning, the user is not logged in 

        # Get show page, the list of notes for an example show
        self.browser.get(self.live_server_url + '/notes/for_show/2')

        # Find and click on 'add note' button
        add_note_link = self.browser.find_element_by_id('add-new-show-link')
        add_note_link.click()

        time.sleep(1)  # FIXME
        
        # Verify at login page
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('alice')
        password.send_keys('qwertyuiop')

        # Click login button
        self.browser.find_element_by_tag_name('button').submit()

        time.sleep(1)  # FIXME

        # Should be logged, and at add note form
        # Find form elements
        title_area = self.browser.find_element_by_id('id_title')
        text_area = self.browser.find_element_by_id('id_text')

        # Check URL (after finding elements, so will know page has loaded)
        self.assertIn('notes/add/2', self.browser.current_url)

        time.sleep(1)  # FIXME
        
        title_area.send_keys('Fab')
        text_area.send_keys('Best ever')
        title_area.submit()  # Convenience method for submitting form with this element in

        # Should now be on note detail page. Title will be 'band at venue by user'
        title = self.browser.find_element_by_id('note-page-title')
        self.assertIn('REM at The Turf Club by alice', title.text)

        note_title = self.browser.find_element_by_id('note-title')
        self.assertIn('Fab', note_title.text)

        note_text = self.browser.find_element_by_id('note-text')
        self.assertIn('Best ever', note_text.text)

        self.assertIn('/notes/detail/5', self.browser.current_url)


    def test_add_note_redirect_to_login_and_register_and_back_to_add_note(self):
        pass

        # start at list of notes

        # click add note

        # verify redirect to login

        # click register link

        # register account

        # verify redirect to add note form

        # enter note text and title

        # verify redirect to note detail 


class RegistrationTests(LiveServerTestCase):

    fixtures = ['fn_testing_users']

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()
    

    def test_login_valid_password(self):

        # Log in
        self.browser.get(self.live_server_url + '/accounts/login')
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('alice')
        password.send_keys('qwertyuiop')

        # Click login button
        self.browser.find_element_by_tag_name('button').submit()

        # Verify page contains 'you are logged in, alice'
        welcome = self.browser.find_element_by_id('welcome-user-msg')
        self.assertIn('You are logged in, alice.', welcome.text)


    def test_login_invalid_password(self):

        # Log in
        self.browser.get(self.live_server_url + '/accounts/login')
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        username.send_keys('none')
        password.send_keys('wrong')

        # Click login button
        self.browser.find_element_by_tag_name('button').submit()

        # Once page loads, check no welcome message
        # find_elements_by_id, returns a list with size 0 if not found, instead of raising an exception
        welcome = self.browser.find_elements_by_id('welcome-user-msg')
        self.assertEqual(len(welcome), 0)

        # Verify page still says 'login or sign up'
        login_invite = self.browser.find_element_by_id('login-or-sign-up')
        self.assertIn('Login or sign up', login_invite.text)
        
        # Verify page does NOT display 'you are logged in, none'
        self.assertNotIn('You are logged in, none.', self.browser.page_source)
        
        # check for error message
        self.assertIn('Please enter a correct username and password', self.browser.page_source)


    def test_register(self):
        pass
        # TODO


class ProfilePageTests(LiveServerTestCase):

    fixtures = [
        'fn_testing_users', 
        'fn_testing_artists', 
        'fn_testing_venues', 
        'fn_testing_shows', 
        'fn_testing_notes'
    ]

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()
    

    def test_view_user_profile_own_notes_shown(self):

        # Get alice's (user 1) profile - one note
        self.browser.get(self.live_server_url + '/user/profile/1')

        title = self.browser.find_element_by_id('username-notes')
        self.assertIn('alice\'s notes', title.text)

        note_divs = self.browser.find_elements_by_class_name('note')
        self.assertEqual(len(note_divs), 1)

        first_note = note_divs[0]
        self.assertIn('ok', first_note.find_element_by_class_name('note-title').text)
        self.assertIn('alright', first_note.find_element_by_class_name('note-text').text)

        self.assertIn('REM at The Turf Club on Jan. 2, 2017', first_note.find_element_by_class_name('note-info').text)
        self.assertIn('Feb. 12, 2017', first_note.find_element_by_class_name('note-posted-at').text)

        # Get dani's profile - no notes
        self.browser.get(self.live_server_url + '/user/profile/4')

        title = self.browser.find_element_by_id('username-notes')
        self.assertIn('dani\'s notes', title.text)

        note_divs = self.browser.find_elements_by_class_name('note')
        self.assertEqual(len(note_divs), 0)
        self.assertIn('No notes', self.browser.find_element_by_id('no-records').text)
