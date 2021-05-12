from django.db import models

from django.db import models
from django.contrib.auth.models import User 
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.storage import default_storage

RATE_CHOICES = (
    ('', ''),
    ("Terrible", "Terrible"),
    ('Bad', 'Bad'),
    ('Not bad', 'Not bad'),
    ('Good', 'Good'),
    ('Great', 'Great'),

)

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

# Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False

""" A music artist """


class Artist(models.Model):
    """ updated model to match API call results """
    name = models.CharField(max_length=50, blank=False)
    hometown = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        artist_string = f'Artist: {self.name} From: {self.hometown} Description: {self.description}'
        return artist_string


""" A venue, that hosts shows. """


class Venue(models.Model):
    """ updated model to match API call results """
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=99, unique=True, blank=False)

    def __str__(self):
        return f'Name: {self.name} Location: {self.address}'


""" A show - one artist playing at one venue at a particular date. """


class Show(models.Model):
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} On: {self.show_date}'


""" One user's opinion of one show. """


class Note(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=50, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True, blank=False)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)  # issue 4 upload photographs with
    # associated notes by chris
    rate = models.CharField(max_length=8, choices=RATE_CHOICES, default='0')

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)

    def __str__(self):

        photo_str = self.photo.url if self.photo else 'no photo'  # issue 4 upload photographs with associated notes
        # by chris
        return f'User: {self.user} Show: {self.show} Note title: {self.title} Text: {self.text} Photo: {photo_str} ' \
               f'Posted on: {self.posted_date} Rated at: {self.Rate}'


"""
A single user.
Instructions for making this work is credited to:
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.TextField(max_length=200, blank=False)
    twitter_username = models.CharField(max_length=15, blank=True)  # Twitter usernames cannot be longer than 15
    # characters
    bio = models.TextField(max_length=1000, blank=True)
    favorite_artist = models.ForeignKey(Artist, blank=True, null=True, on_delete=models.SET_NULL)
    favorite_show = models.ForeignKey(Show, blank=True, null=True, on_delete=models.SET_NULL)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
