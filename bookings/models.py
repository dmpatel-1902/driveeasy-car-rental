from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from cars.models import Car


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    pickup_date = models.DateField()
    return_date = models.DateField()
    pickup_location = models.CharField(max_length=150)
    drop_location = models.CharField(max_length=150)
    total_days = models.PositiveIntegerField(editable=False, default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.pickup_date and self.return_date:
            if self.return_date <= self.pickup_date:
                raise ValidationError('Return date must be after pickup date.')

    def save(self, *args, **kwargs):
        if self.pickup_date and self.return_date:
            self.total_days = max((self.return_date - self.pickup_date).days, 1)
            self.total_amount = self.total_days * self.car.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.pk} - {self.car} by {self.user.username}"
