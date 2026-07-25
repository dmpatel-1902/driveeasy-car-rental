from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car, Category, Review


def home_view(request):
    featured_cars = Car.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    context = {
        'featured_cars': featured_cars,
        'categories': categories,
        'total_cars': Car.objects.count(),
    }
    return render(request, 'home.html', context)


def car_list_view(request):
    cars = Car.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    seats = request.GET.get('seats')
    sort = request.GET.get('sort')

    if query:
        cars = cars.filter(
            Q(brand__icontains=query) | Q(model_name__icontains=query) |
            Q(location__icontains=query)
        )
    if category:
        cars = cars.filter(category__slug=category)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    if seats:
        cars = cars.filter(seats__gte=seats)

    if sort == 'price_low':
        cars = cars.order_by('price_per_day')
    elif sort == 'price_high':
        cars = cars.order_by('-price_per_day')
    elif sort == 'rating':
        cars = cars.order_by('-rating')
    else:
        cars = cars.order_by('-created_at')

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'query': query or '',
        'selected_category': category or '',
        'selected_fuel': fuel_type or '',
        'selected_transmission': transmission or '',
        'total_results': cars.count(),
    }
    return render(request, 'cars/car_list.html', context)


def car_detail_view(request, pk):
    car = get_object_or_404(Car, pk=pk)
    related_cars = Car.objects.filter(category=car.category, is_available=True).exclude(pk=pk)[:3]
    reviews = car.reviews.all()
    context = {
        'car': car,
        'related_cars': related_cars,
        'reviews': reviews,
    }
    return render(request, 'cars/car_detail.html', context)


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        from django.contrib import messages
        messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
    return render(request, 'contact.html')
