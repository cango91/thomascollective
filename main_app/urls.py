from django.urls import path, include
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
	path('trains/', views.train_index, name='index'),
    path('trains/create/', views.TrainCreate.as_view(), name='train_create'),
    path('accounts/signup', views.signup,name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
 ]