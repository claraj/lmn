from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_data(page_num, item_list, num):
    """item_list = list of result object from Django query 
        num = number of item_list per page  
        page_num= integer representing a particular page"""  
    paginator = Paginator(item_list, num)

    try:
        """if the page number exists create a page object that will represent the content 
        # of that particular page"""
        page_obj = paginator.get_page(page_num)

    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        #if the page does not exist get the 1st page by defualt
        page_obj = paginator.page(paginator.num_pages)
        
    return page_obj