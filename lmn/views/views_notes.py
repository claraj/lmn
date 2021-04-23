from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import Note, Show
from ..forms import NewNoteForm 


@login_required
def new_note(request, show_pk):
    """ Create a new Note for a Show """
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)
    else:
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html', {'form': form, 'show': show})


def latest_notes(request):
    """ Get the 20 most recent Notes, ordered with most recent first"""
    notes = Note.objects.all().order_by('-posted_date')[:20]   # the 20 most recent notes
    return render(request, 'lmn/notes/note_list.html', {'notes': notes})


def notes_for_show(request, show_pk): 
    """ Get Notes for one show, most recent first """
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/notes/note_list.html', {'show': show, 'notes': notes})


def note_detail(request, note_pk):
    """ Display one Note """
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html', {'note': note})
