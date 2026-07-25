from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'pickup_date', 'return_date', 'total_amount', 'status')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'car__brand', 'car__model_name')
    list_editable = ('status',)
    date_hierarchy = 'pickup_date'
