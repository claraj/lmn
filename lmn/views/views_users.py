from django.shortcuts import render, redirect
from django.contrib import messages

from ..models import Note, Profile
from ..forms import UserRegistrationForm, UserForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory



def user_profile(request, user_pk):
    # Get user profile for any user on the site
    user = User.objects.get(pk=user_pk)
    user_shows = user.profile.shows_seen.all()
    user_badges = user.profile.badges.all()
    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
    return render(request, 'lmn/users/user_profile.html', { 'user_profile': user, 
                                                            'shows_seen': user_shows, 
                                                            'badges': user_badges, 
                                                            'notes': usernotes})


@login_required() # only logged in users should access this
def edit_user(request, user_pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=user_pk)

    # prepopulate ProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('profile_image', 'shows_seen', 'bio', 'badges'), can_delete=False)
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('user_profile', user_pk=request.user.pk)

        return render(request, 'lmn/users/edit_user.html', { 'user_pk': user_pk,
                                                             'user_form': user_form,
                                                             'formset': formset,
                                                           })
    else:
        raise PermissionDenied


@login_required
def my_user_profile(request):
    if request.user.is_authenticated: # determine the current user and redirect to their user profile
        user_pk = request.user.id
        return redirect('user_profile', user_pk=user_pk)
    else:
        raise PermissionDenied


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            
            if user:
                messages.info(request, 'Thank you, for signing up!')
                login(request, user)

                messages.info(request, 'Account created successfully!')
                return redirect('my_user_profile')

            else:
                messages.add_message(request, messages.ERROR, 'Unable to log in new user')
        else:
            messages.add_message(request, messages.INFO, 'Please check the data you entered')
            # include the invalid form, which will have error messages added to it. The error messages will be displayed by the template.
            return render(request, 'registration/register.html', {'form': form} )

    form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form} )

# create request and render of goodbye html
def goodbye(request):
    logout(request)
    return render(request, 'lmn/users/goodbye_message.html')