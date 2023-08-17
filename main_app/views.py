from django.shortcuts import get_list_or_404, render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.utils.timezone import now
from .models import Train, Route, Booking, Comment, Journey
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


class TrainCreate(CreateView):
    model = Train
    fields = ['name', 'railway', 'capacity', 'cars']
    template_name = 'train/train_form.html'


def train_index(request):
    trains = Train.objects.all()
    return render(request, 'train/index.html', {
        'trains': trains
    })


def train_detail(request, train_id):
    train = Train.objects.get(id=train_id)
    comments = train.comment_set.all()
    form = CommentForm()

    return render(request, 'train/train_detail.html', {'train': train, 'comments': comments, 'form': form})


def update_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = get_object_or_404(Comment, id=pk)
        if form.is_valid():
            if not comment.user == request.user:
                error_msg = "You are not allowed to edit this comment, because it does not belong to you"
                return render(request, 'comment/edit_comment.html', {'form': form, 'comment': comment, 'error': error_msg})
            comment.content = request.POST.get('content')
            comment.rating = request.POST.get('rating')
            comment.date = now()
            comment.save()
            return redirect(reverse('train_detail', kwargs={'train_id': comment.train.id}))
        else:
            error_msg = 'Invalid values'
            return render(request, 'comment/edit_comment.html', {'form': form, 'comment': comment, 'error': error_msg})

    else:
        comment = get_object_or_404(Comment, id=pk)
        comment_dict = {'content': comment.content, 'rating': comment.rating}
        form = CommentForm(comment_dict)
        return render(request, 'comment/edit_comment.html', {'form': form, 'comment': comment})


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'comment/confirm_comment_delete.html'
    success_url = 'https://www.subway.com/en-us'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid Form Data'
    form = UserCreationForm()
    context = {'form': form, 'error': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def add_comment(request, train_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.train = get_object_or_404(Train, id=train_id)
        comment.save()

    return redirect('train_detail', train_id=train_id)


def journey_index(request):
    journeys = Journey.objects.all()
    return render(request, 'journey/journey.html', {
        'journeys': journeys
    })


def journey_detail(request, journey_id):
    journey = get_object_or_404(Journey, id=journey_id)
    stops = journey.route.stationorder_set.all()
    booking_form = BookingForm()
    return render(request, 'journey/journey_detail.html', {'journey': journey, "stops": stops, 'booking_form': booking_form})


@login_required
def create_booking(request, journey_id):
    journey = Journey.objects.get(id=journey_id)
    booking_form = BookingForm(request.POST)
    booking_form.instance.journey = journey
    print(request.user.id)
    booking_form.instance.user = request.user
    if booking_form.is_valid():
        booking_form.save()
        return redirect(reverse('my_bookings'))
    return render(request, 'journey/journey_detail.html', {'journey': journey, 'booking_form': booking_form, 'stops': journey.route.stationorder_set.all(), 'error': 'Invalid Form Data'})


@login_required
def my_bookings(request):
   # journey = Journey.objects.get(id=journey_id)
    allbookings=Booking.objects.filter(user__id=request.user.id)#request.user.booking_set.all()
    print(allbookings)
    return render(request, 'booking/my_bookings.html', {'allbookings':allbookings})

def update_my_bookings(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return ('my_bookings')
    else:
        form = BookingForm(instance=booking)
    return redirect('booking/update_my_bookings.html',{'form':form, 'booking_id':booking_id})


### AJAX ENDPOINTS ###


def getAllStopsForJourney(request, journey_id):
    try:
        route = Journey.objects.get(id=journey_id).route
    except:
        return JsonResponse({'status':404, 'error':'Journey/Route not found'})
    stops = route.stationorder_set.all().values_list('station__name','arrival_time','departure_time')
    stops_list = [{'station': stop[0], 'arrival': stop[1],'departure': stop[2]} for stop in stops]
    return JsonResponse({'status': 200, 'data': {'stops': stops_list, 'route':str(route)},})


def getAllJourneys(request):
    # get query parameters
    sortBy = request.GET.get('sortBy','departure_time')
    order = request.GET.get('order', 'ascending')
    orderStr = f"{'-' if order =='descending'  else ''}{sortBy}"
    
    try:
        journeys = Journey.objects.all().order_by(orderStr)
    except:
        return JsonResponse({'status':404, 'error':'No Journeys in DB'})

    # paginate
    page = request.GET.get('page',1)
    perPage = request.GET.get('limit', 10)
    
    paginator = Paginator(journeys,perPage)
    data = paginator.page(page)    
    
    journeys_list = [{'train': str(journey.train.name), 'route': str(journey.route),
                      'departure': str(journey.departure_time), 'arrival': str(journey.arrival_time), 'id':journey.id} for journey in data]
    return JsonResponse({'status': 200, 'data': journeys_list, 'page':page, 'pageCount':paginator.num_pages, 'limit':perPage })
