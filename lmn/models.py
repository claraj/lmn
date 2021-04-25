from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import datetime

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False


""" A music artist """
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)

    def __str__(self):
        return f'Name: {self.name}'


""" A venue, that hosts shows. """
class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False) 

    def __str__(self):
        return f'Name: {self.name} Location: {self.city}, {self.state}'


""" A show - one artist playing at one venue at a particular date. """
class Show(models.Model):
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} On: {self.show_date}'


""" One user's opinion of one show. """
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True, blank=False)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return f'User: {self.user} Show: {self.show} Note title: {self.title} Text: {self.text} Posted on: {self.posted_date} Image: {self.image}'


class Badge(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'Name: {self.name}, Description: {self.description}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='user_profile_images/', blank=True, null=True)
    shows_seen = models.ManyToManyField(Show)
    bio = models.TextField(blank=True, null=True)
    badges = models.ManyToManyField(Badge)


    def save(self, *args, **kwargs):
        old_profile = Profile.objects.filter(pk=self.pk).first()
        if old_profile and old_profile.profile_image:
            if old_profile.profile_image != self.profile_image:
                self.delete_image(old_profile.profile_image)

        super().save(*args, **kwargs)


    def delete_image(self, image):
        if default_storage.exists(image.name):
            default_storage.delete(image.name)


    def delete(self, *args, **kwargs):
        if self.profile_image:
            self.delete_image(self.profile_image)

        super().delete(*args, **kwargs)


    def __str__(self):
        return f'Name: {self.user.first_name}{self.user.last_name}, Email: {self.user.email}, \
          Profile Image: {self.profile_image}, Shows Seen: {self.shows_seen.all()}, Bio: {self.bio}, \
          Badges: {self.badges.all()}'