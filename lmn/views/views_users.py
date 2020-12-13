from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.dispatch import receiver


from ..models import Venue, Artist, Note, Show, Profile
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_out, user_logged_in



def user_profile(request, user_pk):
    # Get user profile for any user on the site
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
    return render(request, 'lmn/users/user_profile.html', { 'user_profile': user , 'notes': usernotes })


@login_required
def my_user_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        form = UserProfileForm(request.POST, instance=profile) 

        context = {
        'user_form' : form,
        'user_profile': request.user
        }
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            new_user_form = UserProfileForm(instance=request.user.profile)
            return redirect('my_user_profile')
        else:
            messages.error(request, form.errors)
            return render(request, 'lmn/users/profile.html')
            
        return redirect('my_user_profile')
    else:
        profile = Profile.objects.get(user=request.user) #get the current user profile
        reward = ""  
        if profile.note_count: # check if user posted notes
            num_notes = profile.note_count #get the user's number of notes
            reward = decide_reward(num_notes) 
        user_form = UserProfileForm()
    context = {
        'user_form' : user_form,
        'user_profile': request.user,
        'reward': reward
        
    }
    
    return render(request, 'lmn/users/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                login(request, user)
                return redirect('user_profile', user_pk=request.user.pk)
            else:
                messages.add_message(request, messages.ERROR, 'Unable to log in new user')
        else:
            messages.add_message(request, messages.INFO, 'Please check the data you entered')
            # include the invalid form, which will have error messages added to it. The error messages will be displayed by the template.
            return render(request, 'registration/register.html', {'form': form} )

    form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form} )


@receiver(user_logged_out)
def logout_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged out.',   fail_silently=True)

@receiver(user_logged_in)
def login_message(sender, user, request, **kwargs):
    username = user.username
    messages.info(request, 'You have logged in as ' + username.title(),  fail_silently=True)

def decide_reward(num):
    # user gets different rewards based the number of notes they post
    if num > 5: #
        reward = "gold"
    elif num >= 3 and num < 5:
        reward = "silver"
    else:
        reward = "bronze"
    return reward