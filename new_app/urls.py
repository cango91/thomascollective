from django.urls import path
from . import views
	
app_name="dynamic"
urlpatterns = [
	path('', views.train_index, name='index'),
    path('api/trains',views.get_all_trains,name="api.all_trains")
 ]