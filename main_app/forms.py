from django.forms import ModelForm

from .models import Train


class TrainForm(ModelForm):
    class Meta:
        model = train
        fields = '__all__'
