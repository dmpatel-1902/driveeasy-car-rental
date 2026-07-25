from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:car_id>/', views.create_booking_view, name='create_booking'),
    path('detail/<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking_view, name='cancel_booking'),
    path('payment/callback/', views.payment_callback_view, name='payment_callback'),
    path('download-invoice/<int:pk>/', views.download_invoice_view, name='download_invoice'),
]
