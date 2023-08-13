from django.shortcuts import render, redirect
from .models import Train, Schedule, Route, Booking
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login

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


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
