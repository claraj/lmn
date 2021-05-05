from django.shortcuts import render, redirect, get_object_or_404

from ..models import Show
from ..forms import NewShowRatingForm


def save_show_rating(request, show_pk):
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        form = NewShowRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.show = show
            rating.save()
            return redirect('notes_for_show', show_pk=show.pk)
    else:
        form = NewShowRatingForm()
        
    return render(request, 'lmn/notes/note_list.html' , { 'form': form , 'show': show })