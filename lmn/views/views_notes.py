from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show, Profile
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, EmptyPage



@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)

    else:
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form': form , 'show': show })


def latest_notes(request):
    notes = Note.objects.all().order_by('-posted_date')[:100]   # the 100 most recent notes

    paginator = Paginator(notes, 10) # allows only 10 artists to be viewed per page

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
        page = 1
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'lmn/notes/note_list.html', {'notes' : notes, 
                  'page_range': paginator.page_range, 'num_pages' : paginator.num_pages, 
                  'current_page': page})

def most_notes(request):
    shows = Show.objects.annotate(num_notes=Count('note')).order_by('-num_notes')[:10]
    # top 10 shows with most notes
    return render(request, 'lmn/notes/most_notes.html', {'shows': shows })  

def notes_for_show(request, show_pk): 
    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': notes })


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , { 'note': note })


@login_required    
def edit_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if note.user != request.user: # return an error if a user attempts to edit a note that doesn't belong to them
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = NewNoteForm(request.POST, request.FILES, instance=note)

        if form.is_valid(): # if all fields are filled out correctly, save the contents of the form to database
            form.save()

        return redirect('note_detail', note_pk=note_pk)

    else: # this displays the place details if the request method is 'GET' instead of 'POST'
        review_form = NewNoteForm(instance=note) # reuse NewNoteForm for editing notes.
        return render(request, 'lmn/notes/edit_note.html', {'note': note, 'review_form': review_form})
        

@login_required
def delete_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if note.user == request.user:
        note.delete()
        return redirect('user_profile', user_pk=note.user.pk) # redirects to the user's profile after deleting
    else:
        return HttpResponseForbidden()
