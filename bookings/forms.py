from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['pickup_date', 'return_date', 'pickup_location', 'drop_location',
                   'payment_method', 'special_requests']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ahmedabad Airport'}),
            'drop_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ahmedabad Airport'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requirements?'}),
        }
