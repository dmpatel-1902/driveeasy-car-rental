web: python manage.py migrate --run-syncdb && python seed_data.py && gunicorn car_rental.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120
