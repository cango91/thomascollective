from django.urls import path
from .views import verify_email_view

urlpatterns = [
    path('verify_email/<str:token>/', verify_email_view, name='verify_email'),
]