from django.shortcuts import render, redirect, get_object_or_404

from ..models import Venue, Artist, Note, Show
from ..forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, NoteSearchForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from lmn.views.views_paginate import paginate_data


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form': form , 'show': show })


def latest_notes(request):

    form = NoteSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        # Displays all notes by username
        notes = Note.objects.filter(user__username__icontains=search_name).order_by('-posted_date')
    else:
        notes = Note.objects.all().order_by('-posted_date')
        
    #get page number 
    page_number = request.GET.get('page')
    # call paginate data function to implement the pagination
    page_obj = paginate_data(page_number, notes, 4)
    
    context = {
        'notes': notes,
        'form': form, 
        'search_term': search_name,
        'page_obj': page_obj
    }
    
    return render(request, 'lmn/notes/note_list.html', context)




def notes_for_show(request, show_pk): 
    # Notes for show, most recent first
    form = NoteSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        # Displays notes for show by username
        notes = Note.objects.filter(user__username__icontains=search_name).filter(show=show_pk).order_by('-posted_date')
        show = Show.objects.get(pk=show_pk) 
    else:
        notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
        show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': notes, 'form': form, 'search_term': search_name })


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , { 'note': note })


def top_shows(request):
    notes = Note.objects.all().order_by('-rating')
    return render(request, 'lmn/top_shows.html', { 'notes': notes })

# Updates existing note based off instance, checks for matching user/note pk before allowing updates.
@login_required
def update_note(request, show_pk):
    show = Note.objects.get(pk=show_pk)
    form = NewNoteForm(instance=show)
    note = form.save(commit=False)
    if note.user == request.user:
        if request.method == 'POST':
            form = NewNoteForm(request.POST, request.FILES, instance=show)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = request.user
                note.form = form
                note.save()
                return redirect('note_detail', note_pk=note.pk)
    else:
        return HttpResponseForbidden

    return render(request, 'lmn/notes/update_note.html' , { 'form': form , 'show': show })


# Deletes note based off note_pk, checks for matching user/note pk before allowing deletion.
@login_required
def delete_note(request, note_pk): 
    # Notes for show
    note = get_object_or_404(Note, pk=note_pk)
    if note.user == request.user:
        note.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseForbidden


