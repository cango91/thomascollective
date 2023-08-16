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
    path('journeys/<int:journey_id>/booking/new', views.create_booking, name='create_booking')
]
