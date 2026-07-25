from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path("check-username/", views.check_username, name="check_username"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("resend-otp/", views.resend_otp, name="resend_otp"),

    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("forgot-password/verify-otp/", views.forgot_password_verify_otp, name="forgot_password_verify_otp"),
    path("reset-password/", views.reset_password_view, name="reset_password"),

    

]