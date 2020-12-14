from django.db import models
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator



from django.core.files.storage import default_storage
from django.db.models import Count

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False



"""  Profile for User """
class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    favorite_Artist = models.CharField(max_length=200, blank=True)
    favorite_Venue = models.CharField(max_length=200, blank=True)
    favorite_Show = models.CharField(max_length=200, blank=True)
    note_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.favorite_Artist} {self.favorite_Venue} {self.favorite_Show} {self.note_count}'

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

    # making a constrain for a unnique set source:https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
    class Meta:
        unique_together = ('show_date','artist','venue')

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} On: {self.show_date}'


""" One user's opinion of one show. """
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True, blank=False)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    rating = models.IntegerField(default=0, validators = [MaxValueValidator(5), MinValueValidator(1)] ) # Min/Max rating values


    def save(self, *args, **kwargs):
        #count the total number of notes for the current user
        num_notes = Note.objects.filter(user=self.user).count()
        #get current user
        obj = Profile.objects.filter(user=self.user)
        #update the note_count field in the profile model with the user's total number of notes
        obj.update(note_count=num_notes+1)
        #get reference to previous versionof this note
        old_note = Note.objects.filter(pk=self.pk).first()
        if old_note and old_note.photo: #check if an old note exists and has a photo
            if old_note.photo != self.photo: # check if the photo has been changed
                self.delete_photo(old_note.photo) #delete the old photo
        super().save(*args, **kwargs) 

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    #when a Note is deleted, delete the photo file too
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)


    def __str__(self):
        return f'User: {self.user} Show: {self.show} Note title: {self.title} Text: {self.text} Posted on: {self.posted_date} Photo: {self.photo} Rating: {self.rating}'

      
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
