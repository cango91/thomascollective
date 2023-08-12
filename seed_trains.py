import os
import django

trains = [
    {"name": "Thomas", "railway": "TTC", "cars": 5, "capacity": 125, "rating": 4.9},
    {"name": "Subway", "railway": "SEI", "cars": 12, "capacity": 304, "rating": 4.9},
    {"name": "PC-Train", "railway": "SP", "cars": 1, "capacity": 4, "rating": 0.3},
     {"name": "ExpressRail", "railway": "ERL", "cars": 8, "capacity": 220, "rating": 4.6},
    {"name": "MetroMax", "railway": "MMT", "cars": 10, "capacity": 250, "rating": 4.8},
    {"name": "SwiftTransit", "railway": "STC", "cars": 6, "capacity": 160, "rating": 4.7},
    {"name": "UrbanHopper", "railway": "UHR", "cars": 4, "capacity": 110, "rating": 4.5},
    {"name": "CitySprinter", "railway": "CSR", "cars": 7, "capacity": 180, "rating": 4.9},
    {"name": "RapidLink", "railway": "RLK", "cars": 9, "capacity": 230, "rating": 4.7},
    {"name": "TransverseX", "railway": "TXR", "cars": 11, "capacity": 270, "rating": 4.8},
    {"name": "PioneerExpress", "railway": "PEX", "cars": 5, "capacity": 130, "rating": 4.6},
    {"name": "MegaMover", "railway": "MGR", "cars": 12, "capacity": 290, "rating": 4.9},
    {"name": "SpeedStar", "railway": "SSR", "cars": 8, "capacity": 210, "rating": 4.8},
    {"name": "InfinityRail", "railway": "IFR", "cars": 6, "capacity": 170, "rating": 4.7},
    {"name": "MetroSwift", "railway": "MST", "cars": 10, "capacity": 240, "rating": 4.9},
    {"name": "UrbanShuttle", "railway": "USH", "cars": 4, "capacity": 120, "rating": 4.6},
    {"name": "CityExpress", "railway": "CER", "cars": 7, "capacity": 190, "rating": 4.8},
    {"name": "QuickTransit", "railway": "QKT", "cars": 9, "capacity": 220, "rating": 4.7},
    {"name": "MetroFleet", "railway": "MFT", "cars": 11, "capacity": 260, "rating": 4.8},
    {"name": "PrimeLink", "railway": "PLK", "cars": 5, "capacity": 140, "rating": 4.5},
    {"name": "SuperMover", "railway": "SMR", "cars": 12, "capacity": 300, "rating": 4.9},
    {"name": "SwiftWave", "railway": "SWV", "cars": 8, "capacity": 200, "rating": 4.6},
    {"name": "UrbanRider", "railway": "URR", "cars": 6, "capacity": 150, "rating": 4.7},
    {"name": "CityHopper", "railway": "CHR", "cars": 10, "capacity": 230, "rating": 4.8},
    {"name": "RapidExpress", "railway": "REX", "cars": 4, "capacity": 100, "rating": 4.9},
    {"name": "TransitMax", "railway": "TMT", "cars": 7, "capacity": 180, "rating": 4.6},
    {"name": "PioneerLink", "railway": "PLK", "cars": 9, "capacity": 210, "rating": 4.8},
    {"name": "MegaRider", "railway": "MRR", "cars": 11, "capacity": 250, "rating": 4.7},
    {"name": "SpeedTransit", "railway": "STR", "cars": 5, "capacity": 120, "rating": 4.8},
    {"name": "InfiniteRail", "railway": "INR", "cars": 12, "capacity": 280, "rating": 4.9},
    {"name": "MetroZoom", "railway": "MZM", "cars": 8, "capacity": 190, "rating": 4.6},
    {"name": "UrbanExpress", "railway": "UEX", "cars": 6, "capacity": 160, "rating": 4.7},
    {"name": "CitySwift", "railway": "CST", "cars": 10, "capacity": 240, "rating": 4.8},
    {"name": "QuickLink", "railway": "QLK", "cars": 4, "capacity": 110, "rating": 4.9},
    {"name": "TransitWave", "railway": "TWV", "cars": 7, "capacity": 170, "rating": 4.6},
    {"name": "MegaExpress", "railway": "MEX", "cars": 9, "capacity": 200, "rating": 4.8},
    {"name": "SpeedFleet", "railway": "SFT", "cars": 11, "capacity": 260, "rating": 4.7},
    {"name": "RapidMover", "railway": "RMR", "cars": 5, "capacity": 130, "rating": 4.8},
    {"name": "UrbanWave", "railway": "UWV", "cars": 12, "capacity": 290, "rating": 4.9},
    {"name": "CityMax", "railway": "CMX", "cars": 8, "capacity": 210, "rating": 4.6},
    {"name": "MetroRapid", "railway": "MRP", "cars": 6, "capacity": 180, "rating": 4.7},
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
                                 cars=train['cars'], capacity=train['capacity'], rating=train['rating'])
            print(f"Train {train['name']} created")
    print("Trains seeded")
    
print("Seeding Trains")
seed_trains()
