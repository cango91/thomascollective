from django.contrib import admin
from .models import Train, Route, Station, StationOrder, Journey, Booking

# Register your models here.

# admin.site.register(Train)
# admin.site.register(RouteDestinationSchedule)
# admin.site.register(SchedulingInfo)
# admin.site.register(Route)
# admin.site.register(Destination)
admin.site.register(Train)
admin.site.register(Route)
admin.site.register(Station)
admin.site.register(StationOrder)
admin.site.register(Journey)
admin.site.register(Booking)