from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:car_id>/', views.create_booking_view, name='create_booking'),
    path('<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('<int:pk>/cancel/', views.cancel_booking_view, name='cancel_booking'),
]
