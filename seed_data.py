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
from cars.models import Category, Car, CarImage

if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@driveeasy.com', 'admin12345')
    print("Superuser created -> username: admin | password: admin12345")
else:
    print("Superuser 'admin' already exists.")

cats = [
    ('Sedan',     'sedan',     'bi-car-front'),
    ('SUV',       'suv',       'bi-truck'),
    ('Hatchback', 'hatchback', 'bi-car-front-fill'),
    ('Luxury',    'luxury',    'bi-gem'),
    ('Electric',  'electric',  'bi-lightning-charge'),
    ('Van',       'van',       'bi-bus-front'),
]
cat_objs = {}
for name, slug, icon in cats:
    c, _ = Category.objects.get_or_create(name=name, slug=slug, defaults={'icon': icon})
    cat_objs[slug] = c

# (cat_slug, brand, model, year, reg, color, seats, fuel, trans, mileage, price, desc, features, main_image, gallery_images)
cars_data = [
    ('sedan', 'Honda', 'City', 2023, 'GJ01AB1234', 'White', 5, 'petrol', 'automatic', '18 km/l', 2200,
     'Comfortable sedan perfect for city drives and highway trips.',
     'AC, Bluetooth, GPS, Power Steering',
     'cars/Honda_City_front_.jpg',
     ['cars/gallery/Honda_City__BACK_SIDE.jpg', 'cars/gallery/Honda_City__side_.webp', 'cars/gallery/Honda_City_dashboard-18.avif']),

    ('suv', 'Toyota', 'Fortuner', 2023, 'GJ01AB5678', 'Black', 7, 'diesel', 'automatic', '12 km/l', 5500,
     'Powerful SUV with premium comfort for family trips.',
     'AC, Sunroof, GPS, 4WD, Bluetooth',
     'cars/Toyota_Fortuner_front_.avif',
     ['cars/gallery/Toyota_Fortuner_back_.avif', 'cars/gallery/Toyota_Fortuner_side_.avif', 'cars/gallery/Toyota_Fortuner_dashboard-1.avif']),

    ('hatchback', 'Maruti', 'Swift', 2022, 'GJ01AB9012', 'Red', 5, 'petrol', 'manual', '22 km/l', 1500,
     'Compact and fuel-efficient hatchback, great for city commutes.',
     'AC, Bluetooth, Power Windows',
     'cars/Maruti_Swift_front.avif',
     ['cars/gallery/Maruti_Swift_back_side-view.avif', 'cars/gallery/Maruti_Swift_right-side-view.avif', 'cars/gallery/Maruti_Swift_interior-dashboard.avif']),

    ('luxury', 'BMW', '5 Series', 2023, 'GJ01AB3456', 'Grey', 5, 'petrol', 'automatic', '14 km/l', 8500,
     'Luxury sedan with top-notch comfort and performance.',
     'Leather Seats, Sunroof, GPS, Premium Audio',
     'cars/BMW_5_Series_front.jpg',
     ['cars/gallery/BMW_5_Series_back.jpg', 'cars/gallery/BMW_5_Series_side.jpg', 'cars/gallery/BMW_5_Series_interior-dashboard-2.avif']),

    ('electric', 'Tata', 'Nexon EV', 2023, 'GJ01AB7890', 'Blue', 5, 'electric', 'automatic', '312 km range', 3000,
     'Eco-friendly electric SUV with zero emissions.',
     'Fast Charging, AC, GPS, Touchscreen',
     'cars/Tata_Nexon_EV_front.avif',
     ['cars/gallery/Tata_Nexon_EV_back.webp', 'cars/gallery/Tata_Nexon_EV_right-view-120.avif', 'cars/gallery/Tata_Nexon_EV_intr.avif']),

    ('van', 'Toyota', 'Innova Crysta', 2022, 'GJ01AB2345', 'Silver', 8, 'diesel', 'manual', '15 km/l', 3800,
     'Spacious van ideal for group travel and long trips.',
     'AC, Captain Seats, GPS, Bluetooth',
     'cars/Toyota_Innova_Crysta_SOiBruZ.avif',
     ['cars/gallery/Toyota_Innova_Crysta.png', 'cars/gallery/Toyota_Innova_Crysta_back.png', 'cars/gallery/crysta-intr.webp']),

    ('sedan', 'Hyundai', 'Verna', 2023, 'GJ01AB6789', 'White', 5, 'petrol', 'manual', '19 km/l', 2000,
     'Stylish sedan with modern features.',
     'AC, Touchscreen, Bluetooth, Cruise Control',
     'cars/Hyundai_Verna_3U5Geaq.jpg',
     ['cars/gallery/Hyundai_Verna.jpg']),

    ('suv', 'Mahindra', 'Thar Roxx', 2023, 'GJ01AB0123', 'Black', 4, 'diesel', 'manual', '15 km/l', 3200,
     'Rugged off-road SUV for adventure lovers.',
     '4WD, AC, Convertible Top',
     'cars/mahindra-thar-roxx-left-front-three-quarter35_OPSIKLV.avif',
     ['cars/gallery/Mahindra-THAR-ROXXWhite_vvqblXj.avif', 'cars/gallery/thar-roxx-exterior-right-side-view_8lPIvA2.avif', 'cars/gallery/thar-roxx-exterior-right-rear-three-quarter.avif', 'cars/gallery/thar-roxx-dashboard.avif']),

    ('luxury', 'Mercedes', 'C-Class', 2023, 'GJ01AB4567', 'White', 5, 'petrol', 'automatic', '13 km/l', 9000,
     'Premium luxury experience with cutting-edge technology.',
     'Leather Seats, Sunroof, Premium Audio, GPS',
     'cars/Mercedes_C-Class.jpg',
     ['cars/gallery/Mercedes_C-Class.jpg', 'cars/gallery/Mercedes_C-Class__side_.webp', 'cars/gallery/Mercedes_C-Class_back_.jpg']),
]

for cat_slug, brand, model_name, year, reg, color, seats, fuel, trans, mileage, price, desc, features, main_img, gallery_imgs in cars_data:
    car, created = Car.objects.get_or_create(
        registration_number=reg,
        defaults=dict(
            category=cat_objs[cat_slug], brand=brand, model_name=model_name, year=year,
            color=color, seats=seats, fuel_type=fuel, transmission=trans, mileage=mileage,
            price_per_day=price, description=desc, features=features, location='Ahmedabad',
            is_available=True, rating=4.5, image=main_img,
        )
    )
    # Update image if car already existed without one
    if not created and not car.image:
        car.image = main_img
        car.save()

    # Add gallery images if not already present
    if car.gallery.count() == 0:
        for img_path in gallery_imgs:
            CarImage.objects.create(car=car, image=img_path)

print(f"Done! Cars: {Car.objects.count()}, Categories: {Category.objects.count()}")
