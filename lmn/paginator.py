from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, EmptyPage


def paginate(request, model_set, per_page):

    paginator = Paginator(model_set, per_page) # 10 shows per page

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = None

    try:
        model_set = paginator.page(page)
    except PageNotAnInteger:
        model_set = paginator.page(1)
        page = 1
    except EmptyPage:
        model_set = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return model_set, paginator, page