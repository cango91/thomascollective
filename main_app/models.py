from django.db import models
from django.contrib.auth.models import User


class Train(models.Model):
    name = models.CharField(max_length=50)
    railway = models.CharField(max_length=50)
    cars = models.IntegerField()
    capacity = models.IntegerField()
    rating = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)

class Route(models.Model):
    name = models.CharField(max_length= 50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)

class Schedule(models.Model):
    train = models.ForeignKey(
        Train,
        on_delete= models.CASCADE, default = 2
    )
    route = models.ForeignKey(
        Route, 
        on_delete= models.CASCADE, default = 2
    )
    departure_datetime = models.DateField('Departure Date')
    arrival_datetime = models.DateField('Arrival Date')
    base_fare = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)




class Booking(models.Model):
    schedule = models.ForeignKey(
        Schedule, 
        on_delete = models.CASCADE, default = 2
    )
    num_passengers = models.IntegerField()
    fare = models.FloatField()
    luggage_weight = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)

class Destination(models.Model):
    name = models.CharField()
    city = models.CharField()
    state = models.CharField()
    Country = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)


class Comment(models.Model):
    content = models.CharField(max_length=50)
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 2)
 



# Create your models here.
