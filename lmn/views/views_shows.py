from django.shortcuts import render, redirect, get_object_or_404

from ..models import Show, Note
from ..forms import NewShowRatingForm


def show_detail(request, show_pk): 
    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk) 
    rating_form = NewShowRatingForm()
    return render(request, 'lmn/shows/show_detail.html', { 'show': show, 'notes': notes, 'rating_form': rating_form })


def save_show_rating(request, show_pk):
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        form = NewShowRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.show = show
            rating.save()
            return redirect('show_detail', show_pk=show.pk)
    else:
        form = NewShowRatingForm()

    return render(request, 'lmn/notes/show_detail.html' , { 'form': form , 'show': show })