from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import Show, Note, ShowRating
from ..forms import NewShowRatingForm
from ..paginator import paginate
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, EmptyPage

import time


def latest_shows(request):
    shows = Show.objects.all().order_by('-show_date')[:100]

    (shows, paginator, page) = paginate(request, shows, 10)

    return render(request, 'lmn/shows/latest_shows.html', { 'shows' : shows, 
                                                            'page_range': paginator.page_range, 
                                                            'num_pages' : paginator.num_pages, 
                                                            'current_page': page
                                                            })


def show_detail(request, show_pk): 
    # Notes for show, most recent first
    time.sleep(0.01)
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk) 
    
    if request.user.is_authenticated: # if the user is logged in, check to see if they've already rated the show
        user_rating = ShowRating.objects.filter(show=show, user=request.user).first()
        if user_rating:
            user_can_rate = False # don't desplay rating form if the user has already rated the show
        else:
            user_can_rate = True
    else:
        user_can_rate = False # don't show form if user isn't authenticated

    return render(request, 'lmn/shows/show_detail.html', { 'show': show, 'notes': notes, 'user_can_rate': user_can_rate})


@login_required
def save_show_rating(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':

        rating_response = request.POST.get('rating_out_of_five')   
        rating = ShowRating()
        rating.rating_out_of_five = rating_response
        rating.user = request.user
        rating.show = show
        rating.clean_fields()
        rating.save()

    return render(request, 'lmn/shows/show_detail.html', {'show': show})
