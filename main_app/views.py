from decimal import Decimal
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.timezone import now
from .models import StationOrder, Train, Route, Booking, Comment, Journey
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import login, logout
from .forms import CommentForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.core.exceptions import ObjectDoesNotExist
from email_verify.forms import EmailVerificationUserCreationForm
from email_verify.mixins import UserVerifiedMixin

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


class TrainCreate(UserVerifiedMixin, CreateView):
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
    comments = train.comments.all()
    form = CommentForm()

    return render(request, 'train/train_detail.html', {'train': train, 'comments': comments, 'form': form})


def update_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = get_object_or_404(Comment, id=pk)
        if form.is_valid():
            if not comment.user == request.user:
                error_msg = "You are not allowed to edit this comment, because it does not belong to you... AND YOU KNEW IT!"
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
    success_url = reverse_lazy('index')
    
    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object() # This attempts to fetch the object
        except ObjectDoesNotExist:
            # Here you can define what should happen if the object doesn't exist
            # For example, redirecting to another page:
            return redirect('index')
        super().get(request, *args, **kwargs)
        return render(request, self.template_name, {'train': obj.train.id} )
    
        
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            error_msg = "You are not allowed to delete this comment, because it does not belong to you. And you probably know it"
            return render(request, 'comment/confirm_comment_delete.html', {'error': error_msg, 'train': obj.train.id})
        return super().post(request, *args, **kwargs)



def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = EmailVerificationUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except ValidationError as e:
                error_message = f'Email already registered: {e}'
                context = {'form': form, 'error': error_message}
                return render(request, 'registration/signup.html', context)
            login(request, user)
            return redirect('email_verify')
        else:
            error_message = 'Invalid Form Data'
    # if the user is logged in and wants to signup again, log them out first
    if request.user.is_authenticated:
        logout(request)
    form = EmailVerificationUserCreationForm()
    context = {'form': form, 'error': error_message}
    return render(request, 'registration/signup.html', context)

def email_verify(request):
    return render(request, 'email_verify/email_verify.html')



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
    stops = journey.route.station_orders.all()
    booking_form = BookingForm()
    return render(request, 'journey/journey_detail.html', {'journey': journey, "stops": stops, 'booking_form': booking_form})


@login_required
def create_booking(request, journey_id):
    journey = Journey.objects.get(id=journey_id)
    booking_form = BookingForm(request.POST)
    if booking_form.is_valid():
        booking = booking_form.save(commit=False)
        booking.journey = journey
        booking.price = Decimal(booking_form.instance.number_of_passengers * 10.)
        booking.user = request.user
        booking.save()
        return redirect(reverse('my_bookings'))
    return render(request, 'journey/journey_detail.html', {'journey': journey, 'booking_form': booking_form, 'stops': journey.route.station_orders.all(), 'error': 'Invalid Form Data'})


@login_required
def my_bookings(request):
   # journey = Journey.objects.get(id=journey_id)
    allbookings=Booking.objects.filter(user__id=request.user.id)#request.user.booking_set.all()
    return render(request, 'booking/my_bookings.html', {'allbookings':allbookings})

@login_required
def update_my_bookings(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if not request.user == booking.user:
        raise PermissionDenied()
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            # Calculate the price based on the number of passengers
            number_of_passengers = form.cleaned_data['number_of_passengers']
            price_per_passenger = Decimal('10.00')  # Set your own price per passenger
            booking.price = number_of_passengers * price_per_passenger
            
            form.save()

            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/update_my_bookings.html',{'form':form, 'booking_id':booking_id})


class BookingDelete(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/confirm_my_booking_delete.html'
    success_url = reverse_lazy('my_bookings')
    
    ## New code below ##
    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.get_object().user :
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

### CUSTOM ERROR VIEWS FOR PROD ###
def custom_404(request,exception):
    return render(request,'errors/404.html', status=404) 

def custom_500(request):
    return render(request,'errors/500.html', status=500)

def custom_403(request, exception):
    return render(request,'errors/403.html', status=403)

### HELPER SEARCH FUNCTION ###

def searchRoutes(toStop=None, fromStop=None, before=None, after=None):
    station_order_query = StationOrder.objects.all()

    # Handle multiple stops in single stop case using likeness matching
    if (toStop or fromStop) and not (toStop and fromStop):
        stop = toStop or fromStop
        station_order_query = station_order_query.filter(station__name__icontains=stop)

    # Handle multiple stops in to-from case using likeness matching
    if toStop and fromStop:
                # Finding the station orders for 'fromStop' and 'toStop'
        station_orders_before = StationOrder.objects.filter(station__name__icontains=fromStop)
        station_orders_after = StationOrder.objects.filter(station__name__icontains=toStop)

        # Filtering based on the route and order to ensure 'toStop' comes after 'fromStop'
        station_order_query = StationOrder.objects.filter(
            route__in=station_orders_before.values('route'),
            order__gt=Subquery(station_orders_before.filter(route=OuterRef('route')).values('order')),
            id__in=station_orders_after
        )

    routes = Route.objects.filter(station_orders__in=station_order_query).distinct()

    # If filtering by dates, start with Journey model
    journeys_query = Journey.objects.filter(route__in=routes)

    # Apply date filters if provided
    if before:
        journeys_query = journeys_query.filter(departure_time__lt=before)
    if after:
        journeys_query = journeys_query.filter(departure_time__gt=after)

    return journeys_query
### AJAX ENDPOINTS ###


def getAllStopsForJourney(request, journey_id):
    try:
        route = Journey.objects.get(id=journey_id).route
    except Exception as e:
        print(e)
        return JsonResponse({'status':404, 'error':'Journey/Route not found'})
    stops = route.station_orders.all().values_list('station__name','arrival_time','departure_time')
    stops_list = [{'station': stop[0], 'arrival': stop[1],'departure': stop[2]} for stop in stops]
    return JsonResponse({'status': 200, 'data': {'stops': stops_list, 'route':str(route)},})


def getAllJourneys(request):
    # get query parameters
    sortBy = request.GET.get('sortBy','departure_time')
    order = request.GET.get('order', 'ascending')
    orderStr = f"{'-' if order =='descending'  else ''}{sortBy}"
    toDestination = request.GET.get('toStop',None)
    fromDestination = request.GET.get('fromStop',None)
    beforeDate = request.GET.get('before',None)
    afterDate = request.GET.get('after',None)
    try:
        journeys = searchRoutes(toDestination,fromDestination,beforeDate,afterDate).order_by(orderStr)
    except Exception as e:
        print(e)
        return JsonResponse({'status':404, 'error':'No Journeys in DB'})
    # try:
    #     journeys = Journey.objects.all().order_by(orderStr)
    # except:
    #     return JsonResponse({'status':404, 'error':'No Journeys in DB'})

    # paginate
    page = request.GET.get('page',1)
    perPage = request.GET.get('limit', 10)
    
    paginator = Paginator(journeys,perPage)
    data = paginator.page(page)    
    
    journeys_list = [{'train': str(journey.train.name), 'route': str(journey.route),
                      'departure': str(journey.departure_time), 'arrival': str(journey.arrival_time), 'id':journey.id} for journey in data]
    return JsonResponse({'status': 200, 'data': journeys_list, 'page':page, 'pageCount':paginator.num_pages, 'limit':perPage })
