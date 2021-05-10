from django.shortcuts import render, redirect
from django.contrib import messages

from ..models import Venue, Artist, Note, Show, Profile
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ProfileForm, UserForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def goodbye(request):
    logout(request)
    #redirect to sucess page after log out
    return render(request, 'lmn/users/goodbye.html')


def user_profile(request, user_pk):
    # Get user profile for any user on the site
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
    return render(request, 'lmn/users/user_profile.html', { 'user_profile': user, 'notes': usernotes })


@login_required
def my_user_profile(request):
    user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user.profile)
        user_form = UserForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.info(request, 'User profile updated!')
        elif not profile_form.is_valid():
            messages.error(request, profile_form.errors)
        else:
            messages.error(request, user_form.errors)

        usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
        return render(request, 'lmn/users/user_profile.html', { 'user_profile': user, 'notes': usernotes })
    elif request.META.get('HTTP_REFERER') == None or request.META.get('HTTP_REFERER').endswith('accounts/login/'):  # If last page was the login page
        usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
        return render(request, 'lmn/users/user_profile.html', { 'user_profile': user, 'notes': usernotes })
    else:
        profile_form = ProfileForm(instance=user.profile)
        user_form = UserForm(instance=user)
        return render(request, 'lmn/users/my_user_profile.html', { 'my_user_profile': user.profile, 'profile_form': profile_form, 'user_form': user_form })


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


