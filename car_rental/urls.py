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
# Works in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# In production (DEBUG=False), Django's static() helper returns [] so we add it explicitly
if not settings.DEBUG:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
