from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import Show, Note, ShowRating
from ..forms import NewShowRatingForm


def show_detail(request, show_pk): 
    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk) 
    
    if request.user.is_authenticated:
        user_rating = ShowRating.objects.filter(show=show, user=request.user).first()
        if user_rating:
            rating_form = None
        else:
            rating_form = NewShowRatingForm()
    else:
        rating_form = None
    return render(request, 'lmn/shows/show_detail.html', { 'show': show, 'notes': notes, 'rating_form': rating_form })


@login_required
def save_show_rating(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        rating_form = NewShowRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.show = show
            rating.save()
            return redirect('show_detail', show_pk=show.pk)
    else:
        form = NewShowRatingForm()

    return render(request, 'lmn/shows/show_detail.html' , { 'rating_form': rating_form , 'show': show })