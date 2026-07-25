"""
Sample data seeder script.
Run this AFTER migrations to populate the database with demo categories, cars, and a superuser.

Usage:
    python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental.settings')
django.setup()

from accounts.models import CustomUser
from cars.models import Category, Car

if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@driveeasy.com', 'admin12345')
    print("Superuser created -> username: admin | password: admin12345")
else:
    print("Superuser 'admin' already exists.")

cats = [
    ('Sedan', 'sedan', 'bi-car-front'),
    ('SUV', 'suv', 'bi-truck'),
    ('Hatchback', 'hatchback', 'bi-car-front-fill'),
    ('Luxury', 'luxury', 'bi-gem'),
    ('Electric', 'electric', 'bi-lightning-charge'),
    ('Van', 'van', 'bi-bus-front'),
]
cat_objs = {}
for name, slug, icon in cats:
    c, _ = Category.objects.get_or_create(name=name, slug=slug, defaults={'icon': icon})
    cat_objs[slug] = c

cars_data = [
    ('sedan', 'Honda', 'City', 2023, 'GJ01AB1234', 'White', 5, 'petrol', 'automatic', '18 km/l', 2200,
     'Comfortable sedan perfect for city drives and highway trips.', 'AC, Bluetooth, GPS, Power Steering'),
    ('suv', 'Toyota', 'Fortuner', 2023, 'GJ01AB5678', 'Black', 7, 'diesel', 'automatic', '12 km/l', 5500,
     'Powerful SUV with premium comfort for family trips.', 'AC, Sunroof, GPS, 4WD, Bluetooth'),
    ('hatchback', 'Maruti', 'Swift', 2022, 'GJ01AB9012', 'Red', 5, 'petrol', 'manual', '22 km/l', 1500,
     'Compact and fuel-efficient hatchback, great for city commutes.', 'AC, Bluetooth, Power Windows'),
    ('luxury', 'BMW', '5 Series', 2023, 'GJ01AB3456', 'Grey', 5, 'petrol', 'automatic', '14 km/l', 8500,
     'Luxury sedan with top-notch comfort and performance.', 'Leather Seats, Sunroof, GPS, Premium Audio'),
    ('electric', 'Tata', 'Nexon EV', 2023, 'GJ01AB7890', 'Blue', 5, 'electric', 'automatic', '312 km range', 3000,
     'Eco-friendly electric SUV with zero emissions.', 'Fast Charging, AC, GPS, Touchscreen'),
    ('van', 'Toyota', 'Innova Crysta', 2022, 'GJ01AB2345', 'Silver', 8, 'diesel', 'manual', '15 km/l', 3800,
     'Spacious van ideal for group travel and long trips.', 'AC, Captain Seats, GPS, Bluetooth'),
    ('sedan', 'Hyundai', 'Verna', 2023, 'GJ01AB6789', 'White', 5, 'petrol', 'manual', '19 km/l', 2000,
     'Stylish sedan with modern features.', 'AC, Touchscreen, Bluetooth, Cruise Control'),
    ('suv', 'Mahindra', 'Thar', 2023, 'GJ01AB0123', 'Black', 4, 'diesel', 'manual', '15 km/l', 3200,
     'Rugged off-road SUV for adventure lovers.', '4WD, AC, Convertible Top'),
    ('luxury', 'Mercedes', 'C-Class', 2023, 'GJ01AB4567', 'White', 5, 'petrol', 'automatic', '13 km/l', 9000,
     'Premium luxury experience with cutting-edge technology.', 'Leather Seats, Sunroof, Premium Audio, GPS'),
]

for cat_slug, brand, model_name, year, reg, color, seats, fuel, trans, mileage, price, desc, features in cars_data:
    Car.objects.get_or_create(
        registration_number=reg,
        defaults=dict(
            category=cat_objs[cat_slug], brand=brand, model_name=model_name, year=year,
            color=color, seats=seats, fuel_type=fuel, transmission=trans, mileage=mileage,
            price_per_day=price, description=desc, features=features, location='Ahmedabad',
            is_available=True, rating=4.5,
        )
    )

print(f"Done! Total cars: {Car.objects.count()}, Total categories: {Category.objects.count()}")
