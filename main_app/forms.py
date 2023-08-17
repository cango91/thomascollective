from django import forms

from .models import Train, Comment, Booking


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'

class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'star-rating star-rating-editable'}))
    class Meta:
        model = Comment
        fields = ['content', 'rating']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat_number', 'number_of_passengers', 'luggage_weight']
