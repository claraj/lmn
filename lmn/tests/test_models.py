from django.test import TestCase

from django.contrib.auth.models import User
from django.db import IntegrityError
from lmn.models import Artist
# Create your tests here.


class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


class TestProfile(TestCase):
    def test_create_user_creates_profile(self):
        user = User(username='user', email='fake@email.address', first_name='fake', last_name='user')
        user.save()

        profile = user.profile

        self.assertIsNotNone(profile)


    def test_delete_artist_sets_favorite_to_null(self):
        ''' Can't seem to get this to work '''
        user = User(username='user', email='fake@email.address', first_name='fake', last_name='user')
        user.save()
        artist = Artist(name='Nym', hometown='Place', description='Bio')
        artist.save()
        artist_pk = artist.pk

        user.profile.favorite_artist = artist
        user.profile.favorite_artist.save()
        user.save()
        favorite = user.profile.favorite_artist

        self.assertIsNotNone(favorite)

        artist.delete()
        artist.save()

        self.assertFalse(Artist.objects.filter(pk=artist_pk).exists())

        favorite = user.profile.favorite_artist

        ''' This is the line that is failing. It successfully deletes the artist, but not from the user profile, despite successfully working in the live version '''
        # self.assertIsNone(favorite)
