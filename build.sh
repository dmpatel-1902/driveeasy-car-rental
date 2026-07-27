#!/usr/bin/env bash
# Render build script
set -e  # exit on error

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --run-syncdb

# Clear existing car/category data and re-seed with correct image paths
python manage.py shell -c "
from cars.models import Car, CarImage, Category
CarImage.objects.all().delete()
Car.objects.all().delete()
Category.objects.all().delete()
print('Cleared cars, gallery, categories for fresh seed.')
"
python seed_data.py
