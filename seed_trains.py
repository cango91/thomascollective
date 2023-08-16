import os
import django

trains = [
    {"name": "Thomas", "railway": "TTC", "cars": 5, "capacity": 125, "rating": 4.9},
    {"name": "Subway", "railway": "SEI", "cars": 12, "capacity": 304, "rating": 4.9},
    {"name": "PC-Train", "railway": "SP", "cars": 1, "capacity": 4, "rating": 0.3},
    {"name": "Panda Express", "railway": "PET", "cars": 10, "capacity": 250, "rating": 5.0},

]

os.environ.setdefault('DJANGO_SETTINGS_MODULE','thomascollective.settings')
django.setup()

from main_app.models import Train

def seed_trains():
    for train in trains:
        try:
            t = Train.objects.get(name=train['name'])
            print(f"train named {train['name']} already exists with id: {t.id}")
        except Train.DoesNotExist as e:
            Train.objects.create(name=train['name'], railway=train['railway'],
                                 cars=train['cars'], capacity=train['capacity'])
            print(f"Train {train['name']} created")
    print("Trains seeded")
    
print("Seeding Trains")
seed_trains()
