from django.contrib import admin
<<<<<<< HEAD
from .models import Train, Route, Destination, RouteDestinationSchedule
=======
from .models import Train, Route, Destination, RouteDestinationSchedule, SchedulingInfo
>>>>>>> main

# Register your models here.

admin.site.register(Train)
admin.site.register(RouteDestinationSchedule)
<<<<<<< HEAD
=======
admin.site.register(SchedulingInfo)
>>>>>>> main
admin.site.register(Route)
admin.site.register(Destination)