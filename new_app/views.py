from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render, get_list_or_404
from main_app.models import Train

# Create your views here.


def train_index(req):
    return render(req, 'index.html')

# API endpoints. For dynamic-table demonstration

def get_all_trains(request):
    # Our front-end fetch function will be sending us pagination parameters,
    # As well as sorting parameters. We should extract them and use it in our Query

    # name is default if we don't get a sortBy parameter
    sortBy = request.GET.get('sortBy', 'name')
    sortAscending = request.GET.get('order', False) == 'ascending'
    sort_field = f"{'-' if not sortAscending else ''}{sortBy}"
    trains = Train.objects.all().order_by(sort_field)

    # Luckily awesomest framework Django already provides a paginator for us so no need to custom query :)
    # (in express I had to do a bunch of maths :D)

    perPage = int(request.GET.get('limit', '10'))
    page = int(request.GET.get('page', '1'))

    paginator = Paginator(trains, perPage)

    total_pages = paginator.num_pages if perPage > 0 else 1
    
    # Get the requested page's data
    try:
        current_page_data = paginator.page(page)
    except EmptyPage:
        return JsonResponse({
            'error': 'Invalid page number',
            'status': 'error'
        }, status=400)
        
    serialized_train_data = serialize('json',current_page_data) # LOVE YOU DJANGOOOO!!!
        
    # Create the JSON response
    response_data = {
        'page': page,
        'pageCount': total_pages,
        'perPage': perPage,
        'status': 'success',
        'data': serialized_train_data
    }
    
    return JsonResponse(response_data)
