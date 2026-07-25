from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars import views as car_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', car_views.home_view, name='home'),
    path('about/', car_views.about_view, name='about'),
    path('contact/', car_views.contact_view, name='contact'),
    path('cars/', include('cars.urls')),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
]

# Always serve media files (uploaded car images, profile pics)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
