from django.db import models
from django.contrib.auth.models import User

# Remember that every model gets a primary key field by default.

# The User model is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

# And, require email, first name, and last name for each user
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False


class Artist(models.Model):
    """ Represents a musician or a band - a music artist """
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'Name: {self.name}'


class Venue(models.Model):
    """ Represents a place that Shows take place at. """
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)

    def __str__(self):
        return f'Name: {self.name} Location: {self.city}, {self.state}'


class Show(models.Model):
    """ One Artist playing at one Venue at a particular date and time. """
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} On: {self.show_date}'


class Note(models.Model):
    """ One User's opinion of one Show. """
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f'User: {self.user} Show: {self.show} Note title: {self.title} \
        Text: {self.text} Posted on: {self.posted_date}'
