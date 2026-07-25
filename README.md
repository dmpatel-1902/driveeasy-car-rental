# DriveEasy — Car Rental Web App (Django)

Ek complete, fully-responsive **Car Rental** website Django me bana hai. Bootstrap 5 use kiya gaya hai, isliye ye mobile, tablet, aur desktop sab par sahi se dikhega.

## Features / Modules

1. **Accounts App** — Custom user model (phone, address, driving license, profile picture), register, login, logout, profile edit.
2. **Cars App** — Categories (Sedan, SUV, Hatchback, Luxury, Electric, Van), car listing with search + multi-filter (category, fuel type, transmission, price range, seats), sorting, pagination, car detail page with gallery + reviews.
3. **Bookings App** — Date-based booking form, automatic total-days & total-amount calculation, booking detail/invoice page, "My Bookings" dashboard, booking cancellation.
4. **Admin Panel** — Full Django admin for managing users, categories, cars (with inline image gallery), and bookings (editable status).
5. **Responsive UI** — Custom CSS + Bootstrap 5 + Bootstrap Icons. Hero section, category pills, car cards, filter sidebar, sticky navbar — sab responsive hain (mobile pe navbar collapse hota hai).
6. **Home, About, Contact** pages included.

## Project Structure

```
car_rental_project/
├── manage.py
├── seed_data.py          # demo data + superuser seeder
├── car_rental/            # project settings/urls
├── accounts/               # custom user, auth
├── cars/                   # categories, cars, reviews
├── bookings/                # booking system
├── templates/               # all HTML templates
├── static/css/style.css     # custom responsive styling
└── media/                    # uploaded images (cars, profile pics)
```

## Setup Instructions

1. **Install dependencies** (Python 3.10+ recommended):
   ```bash
   pip install django
   ```

2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Seed demo data** (creates admin user + sample cars/categories):
   ```bash
   python seed_data.py
   ```
   This creates a superuser: **username:** `admin`  **password:** `admin12345`

   (Alternatively skip this and run `python manage.py createsuperuser` yourself.)

4. **Run the server:**
   ```bash
   python manage.py runserver
   ```

5. Visit **http://127.0.0.1:8000/** for the site, and **http://127.0.0.1:8000/admin/** for the admin panel.

## Adding Your Own Cars

Go to `/admin/` → login as admin → **Cars** section → **Add Car**. Upload an image, set price/day, category, features (comma-separated), etc. It will automatically show up on the site.

## Notes

- `DEBUG = True` hai — production me deploy karne se pehle `SECRET_KEY` change karein, `DEBUG = False` karein, aur `ALLOWED_HOSTS` set karein.
- Payment is a simple method-selector (COD / Card / UPI) — koi real payment gateway integrate nahi hai; agar chahiye to Razorpay/Stripe add kiya ja sakta hai.
- Images `media/` folder me store hoti hain — production me S3 ya kisi cloud storage use karna recommended hai.
