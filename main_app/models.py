from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class Train(models.Model):
    name = models.CharField(max_length=50)
    railway = models.CharField(max_length=50)
    cars = models.IntegerField()
    capacity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def get_rating(self):
        ratings = self.comments.all().values_list('rating', flat=True)
        count = len(ratings)
        return sum(ratings) / count if count else 0

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('train_detail', kwargs={'train_id': self.id})

class Comment(models.Model):
    train = models.ForeignKey(Train, related_name='comments', on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=250)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    
    def get_absolute_url(self):
        return reverse('train_detail', kwargs={'train_id': self.train.id})

class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    distance = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    
    def __str__(self):
        station_names = [order.station.name for order in self.station_orders.all()]
        if len(station_names) >= 2:
            return f"{station_names[0]} to {station_names[-1]}"
        return 'No Route Planned'
    
class StationOrder(models.Model):
    route = models.ForeignKey(Route, related_name='station_orders', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.route.train.name}: {self.station}"
    
class Journey(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    route = models.OneToOneField(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    def __str__(self):
        station_names = [order.station.name for order in self.route.station_orders.all()]
        if len(station_names) > 1:
            return f"{self.train} - {station_names[0]} to {station_names[-1]}"
        return 'No Route Planned'
    
class Booking(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)
    seat_number = models.CharField(max_length=10, default='A1')
    booking_time = models.DateTimeField(default=now)
    number_of_passengers = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    luggage_weight = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username} - {self.journey}"

    
class Station(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name
