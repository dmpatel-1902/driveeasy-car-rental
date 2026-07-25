from django.contrib import admin
from .models import Category, Car, CarImage, Review


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'category', 'price_per_day',
                     'is_available', 'location', 'rating')
    list_filter = ('category', 'fuel_type', 'transmission', 'is_available', 'location')
    search_fields = ('brand', 'model_name', 'registration_number')
    list_editable = ('is_available', 'price_per_day')
    inlines = [CarImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
