from django.contrib import admin
from .models import Train, Route, Destination

# Register your models here.

admin.site.register(Train)
# admin.site.register(Schedule)
admin.site.register(Route)
admin.site.register(Destination)