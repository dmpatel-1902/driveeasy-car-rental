from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='bi-car-front', help_text="Bootstrap icon class")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(models.Model):
    FUEL_CHOICES = (
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    )
    TRANSMISSION_CHOICES = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=50)
    seats = models.PositiveIntegerField(default=4)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    mileage = models.CharField(max_length=50, blank=True, help_text="e.g. 18 km/l")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="Comma separated features e.g. AC, GPS, Bluetooth")
    location = models.CharField(max_length=100, default='Ahmedabad')
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5,
                                   validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.year})"

    def get_absolute_url(self):
        return reverse('cars:car_detail', kwargs={'pk': self.pk})

    def feature_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='cars/gallery/')

    def __str__(self):
        return f"Image for {self.car}"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.car} ({self.rating}★)"
