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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)

    def get_rating(self):
        # get all comments for this trains 'rating' field, and give it as a flat list (default gives a list of tuples)
        ratings_list = self.comment_set.all().values_list('rating', flat=True)
        count = len(ratings_list)
        if not count:
            return 0
        total_rating = sum(ratings_list)
        average_rating = total_rating / count
        return average_rating

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('train_detail', kwargs={'train_id': self.id})

class Route(models.Model):
    name = models.CharField(max_length= 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, default = 1)

    def __str__(self):
        return self.name

# class Schedule(models.Model):
#     train = models.ForeignKey(
#         Train,
#         on_delete= models.CASCADE, default = 2
#     )
#     route = models.ForeignKey(
#         Route, 
#         on_delete= models.CASCADE, default = 2
#     )
#     departure_datetime = models.DateField('Departure Date')
#     arrival_datetime = models.DateField('Arrival Date')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)
    

class SchedulingInfo(models.Model):
    arrival = models.DateTimeField(blank=True, null=True)
    departure = models.DateTimeField(blank=True, null=True)


class Booking(models.Model):
    # schedule = models.ForeignKey(
    #     Schedule, 
    #     on_delete = models.CASCADE, default = 2
    #)
    num_passengers = models.IntegerField()
    fare = models.FloatField()
    luggage_weight = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, default = 1)

class Destination(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)
    routes = models.ManyToManyField(Route, through='RouteDestinationSchedule')

    def __str__(self):
        return self.name


class Comment(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=250)
    rating = models.IntegerField(validators= [MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)
    
    def get_absolute_url(self):
        return reverse('train_detail', kwargs={'train_id': self.train.id})


class RouteDestinationSchedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    scheduling_info = models.ForeignKey(SchedulingInfo,on_delete=models.PROTECT,blank=True,null=True)



# Create your models here.
