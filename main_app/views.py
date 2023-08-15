from django.shortcuts import render, redirect
from .models import Train, Schedule, Route, Booking, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def home(request):
    return render(request, 'home.html')
 
class TrainCreate(CreateView):
    model = Train
    fields = ['name', 'railway','capacity', 'cars']
    template_name = 'train/train_form.html'

def train_index(request):
    trains = Train.objects.all()
    return render(request, 'train/index.html', {
        'trains': trains
    } )

def train_detail(request, train_id):
    train = Train.objects.get(id=train_id)
    Comments = train.comment_set.all()
    form = CommentForm()

    return render(request, 'train/train_detail.html', {'train': train, 'form': form})

class CommentUpdate(UpdateView):
   model = Comment
   fields = ['content', 'rating']
   template_name = 'comment/edit_comment.html'
   
class CommentDelete(DeleteView):
   model = Comment
   template_name = 'comment/confirm_comment_delete.html'
   success_url = 'https://www.subway.com/en-us?utm_source=bing&utm_medium=cpc&utm_term=subway%20com_exact&utm_content=brand&utm_campaign=&cid=0:0:00:0:nat-us:0&0=0&gclid=eda71fd3e2d01efd63ec7b08791cf243&gclsrc=3p.ds&msclkid=eda71fd3e2d01efd63ec7b08791cf243'


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

@login_required
def add_comment(request, train_id):
   form = CommentForm(request.POST)
   if form.is_valid():
      comment = form.save(commit= False)
      comment.user = request.user
      comment.save()


      return redirect('train_detail', train_id=train_id)
