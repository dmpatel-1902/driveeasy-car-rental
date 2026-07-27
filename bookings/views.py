import requests
import uuid
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from cars.models import Car
from .models import Booking
from .forms import BookingForm

def create_cashfree_order(booking, request):
    env = getattr(settings, 'CASHFREE_ENV', 'SANDBOX').upper()
    client_id = getattr(settings, 'CASHFREE_CLIENT_ID', '')
    client_secret = getattr(settings, 'CASHFREE_CLIENT_SECRET', '')

    base_url = (
        "https://sandbox.cashfree.com/pg/orders"
        if env == 'SANDBOX'
        else "https://api.cashfree.com/pg/orders"
    )

    order_id = f"ORDER_{booking.id}_{uuid.uuid4().hex[:8]}"
    booking.cashfree_order_id = order_id
    booking.save()

    phone = str(getattr(booking.user, 'phone', '') or '9999999999').strip()
    if not phone.isdigit() or len(phone) < 10:
        phone = '9999999999'
    email = booking.user.email or "customer@example.com"
    name  = (booking.user.get_full_name() or booking.user.username)[:50]

    payload = {
        "order_amount":   float(booking.total_amount),
        "order_currency": "INR",
        "order_id":       order_id,
        "customer_details": {
            "customer_id":    f"CUST_{booking.user.id}",
            "customer_phone": phone,
            "customer_email": email,
            "customer_name":  name,
        },
        "order_meta": {
            "return_url": request.build_absolute_uri(
                f"/bookings/payment/callback/?order_id={order_id}"
            )
        },
    }

    headers = {
        "accept":           "application/json",
        "content-type":     "application/json",
        "x-api-version":    "2023-08-01",
        "x-client-id":      client_id,
        "x-client-secret":  client_secret,
    }

    try:
        response = requests.post(base_url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json().get('payment_session_id')
        # Log the full error so it shows in the dev-server console
        print(f"[Cashfree] Order creation failed — HTTP {response.status_code}: {response.text}")
    except requests.RequestException as exc:
        print(f"[Cashfree] Network error while creating order: {exc}")

    return None

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

            if booking.payment_method in ['card', 'upi']:
                payment_session_id = create_cashfree_order(booking, request)
                if payment_session_id:
                    # Pass the session ID to a template that will trigger Cashfree SDK
                    cf_env = getattr(settings, 'CASHFREE_ENV', 'SANDBOX').upper()
                    return render(request, 'bookings/cashfree_checkout.html', {
                        'payment_session_id': payment_session_id,
                        'cf_mode': 'sandbox' if cf_env == 'SANDBOX' else 'production',
                    })
                else:
                    messages.error(request, 'Error initializing payment gateway. Please try again or choose Cash on Delivery.')
                    booking.delete() # Rollback booking if payment fails to initialize
                    return redirect('cars:car_detail', pk=car_id)

            messages.success(request, f'Booking confirmed! Your booking ID is #{booking.pk}.')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form, 'car': car})

@login_required
def payment_callback_view(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        messages.error(request, "Invalid payment request.")
        return redirect('home')
        
    booking = get_object_or_404(Booking, cashfree_order_id=order_id)
    
    # Verify order status with Cashfree
    env = getattr(settings, 'CASHFREE_ENV', 'SANDBOX').upper()
    client_id = getattr(settings, 'CASHFREE_CLIENT_ID', '')
    client_secret = getattr(settings, 'CASHFREE_CLIENT_SECRET', '')
    url = (
        f"https://sandbox.cashfree.com/pg/orders/{order_id}"
        if env == 'SANDBOX'
        else f"https://api.cashfree.com/pg/orders/{order_id}"
    )

    headers = {
        "accept":          "application/json",
        "x-api-version":   "2023-08-01",
        "x-client-id":     client_id,
        "x-client-secret": client_secret,
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        order_status = data.get('order_status')
        if order_status == 'PAID':
            booking.payment_status = 'SUCCESS'
            booking.status = 'confirmed'
            booking.save()
            messages.success(request, f'Payment successful! Your booking ID is #{booking.pk}.')
        else:
            booking.payment_status = 'FAILED'
            booking.save()
            messages.error(request, 'Payment failed or is still pending. Please check your bookings.')
    else:
        messages.error(request, 'Could not verify payment status.')
        
    return redirect('bookings:booking_detail', pk=booking.pk)


@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def download_invoice_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    template = get_template('bookings/invoice_pdf.html')
    context = {'booking': booking}
    html = template.render(context)
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Invoice_Booking_{booking.id}.pdf"'
        return response
    return HttpResponse('Error generating PDF invoice', status=400)


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

