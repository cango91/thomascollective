from django.forms import ModelForm

from .models import Train, Comment


class TrainForm(ModelForm):
    class Meta:
        model = Train
        fields = '__all__'

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content', 'rating']