from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cars.models import Car
from .models import Booking
from .forms import BookingForm


@login_required
def create_booking_view(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if not car.is_available:
        messages.error(request, 'Sorry, this car is currently not available for booking.')
        return redirect('cars:car_detail', pk=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.full_clean()
            booking.save()
            messages.success(request, f'Booking confirmed! Your booking ID is #{booking.pk}.')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form, 'car': car})


@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('bookings:my_bookings')
