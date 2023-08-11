from django.shortcuts import render, redirect
from .models import Train, Schedule, Route, Booking
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def home(request):
    return render(request, 'home.html')
 
class TrainCreate(CreateView):
    model = Train
    fields = '__all__'

def train_index(request):
    trains = Train.objects.all()
    return render(request, 'train/index.html', {
        'trains': trains
    } )