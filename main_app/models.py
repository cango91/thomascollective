from django.db import models


class Train(models.Model):
    name = models.CharField(max_length=50)
    railway = models.CharField(max_length=50)
    cars = models.IntegerField()
    capacity = models.IntegerField()
    rating = models.FloatField()

class Route(models.Model):
    name = models.CharField(max_length= 50)

class Schedule(models.Model):
    train = models.ForeignKey(
        Train,
        on_delete= models.CASCADE
    )
    route = models.ForeignKey(
        Route, 
        on_delete= models.CASCADE
    )
    departure_datetime = models.DateField('Departure Date')
    arrival_datetime = models.DateField('Arrival Date')
    base_fare = models.IntegerField()




class Booking(models.Model):
    schedule = models.ForeignKey(
        Schedule, 
        on_delete = models.CASCADE
    )
    num_passengers = models.IntegerField()
    fare = models.FloatField()
    luggage_weight = models.FloatField()

class Destination(models.Model):
    name = models.CharField()
    city = models.CharField()
    state = models.CharField()
    Country = models.CharField()


class Comment(models.Model):
    content = models.CharField()
    rating = models.IntegerField()
 



# Create your models here.
