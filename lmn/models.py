from django.db import models

from django.db import models
from django.contrib.auth.models import User
import datetime

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
    name = models.CharField(max_length=200, blank=True)
    hometown = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        artist_string = f'Artist: {self.name} From: {self.hometown} Description: {self.description}'
        return artist_string


""" A venue, that hosts shows. """


class Venue(models.Model):
    """ updated model to match API call results """
    name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=400, unique=True, blank=True)

    def __str__(self):
        return f'Name: {self.name} Location: {self.address}'


""" A show - one artist playing at one venue at a particular date. """


class Show(models.Model):
    show_date = models.DateTimeField(blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} On: {self.show_date}'


""" One user's opinion of one show. """


class Note(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(max_length=1000, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'User: {self.user} Show: {self.show} Note title: {self.title} Text: {self.text} Posted on: {self.posted_date}'
