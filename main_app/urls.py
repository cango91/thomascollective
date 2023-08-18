from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('trains/', views.train_index, name='index'),
    path('trains/create/', views.TrainCreate.as_view(), name='train_create'),
    path('accounts/signup', views.signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('trains/<int:train_id>/', views.train_detail, name='train_detail'),
    path('trains/<int:train_id>/comment', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/update', views.update_comment, name='update_comment'),
    path('comment/<int:pk>/delete', views.CommentDelete.as_view(), name='delete_comment'),
    path('journeys/', views.journey_index, name='journey_index'),
    path('journeys/<int:journey_id>/', views.journey_detail, name='journey_detail'),
    path('journeys/<int:journey_id>/booking/new', views.create_booking, name='create_booking'),
    path('booking/my_bookings', views.my_bookings, name='my_bookings'),
    path('ajax/journeys/<int:journey_id>/stops', views.getAllStopsForJourney, name='all_stops_for_journey'),
    path('ajax/journeys/', views.getAllJourneys, name='all_journeys'),
    path('booking/my_bookings/<int:booking_id>/update', views.update_my_bookings, name='update_my_bookings'),
    path('mybookings/<int:pk>/delete', views.BookingDelete.as_view(), name='delete_booking'),
    path('email_verify/', views.email_verify, name='email_verify'),
]
