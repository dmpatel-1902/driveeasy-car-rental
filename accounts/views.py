from .utils import send_otp_email
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserUpdateForm, StyledAuthenticationForm, StyledSetPasswordForm
from bookings.models import Booking
from django.contrib.auth import get_user_model
from .models import EmailOTP
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            if User.objects.filter(email=email).exists():

                messages.error(request, "Email already registered.")

                return render(
                    request,
                    "accounts/register.html",
                    {"form": form}
                )

            request.session["register_data"] = {

                "username": form.cleaned_data["username"],
                "email": email,
                "phone_number": form.cleaned_data["phone_number"],
                "password": form.cleaned_data["password1"],

            }

            send_otp_email(email)

            return redirect("accounts:verify_otp")

    else:

        form = CustomUserCreationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = StyledAuthenticationForm

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Welcome back, {form.get_user().username}!"
        )
        return super().form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:10]
    context = {
        'form': form,
        'bookings': bookings,
        'total_bookings': Booking.objects.filter(user=request.user).count(),
    }
    return render(request, 'accounts/profile.html', context)


def check_username(request):
    username = request.GET.get("username", "").strip().lower()

    if username == "":
        return JsonResponse({
            "available": False,
            "suggestions": []
        })

    exists = User.objects.filter(username__iexact=username).exists()

    suggestions = []

    if exists:

        while len(suggestions) < 5:

            option = random.choice([
                f"{username}{random.randint(1,999)}",
                f"{username}_{random.randint(10,99)}",
                f"{username}official",
                f"real_{username}",
                f"{username}.patel",
                f"{username}2026",
                f"mr_{username}",
                f"iam{username}"
            ])

            if not User.objects.filter(username__iexact=option).exists():
                if option not in suggestions:
                    suggestions.append(option)

    return JsonResponse({
        "available": not exists,
        "suggestions": suggestions
    })

def verify_otp(request):

    register_data = request.session.get("register_data")

    if not register_data:
        messages.error(request, "Session expired. Please register again.")
        return redirect("accounts:register")

    email = register_data["email"]

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        otp_obj = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        if not otp_obj:
            messages.error(request, "OTP not found. Please register again.")
            return redirect("accounts:register")

        if otp_obj.is_expired():
            messages.error(request, "OTP has expired. Please request a new one.")
            return render(request, "accounts/verify_otp.html", {"email": email})

        if entered_otp != otp_obj.otp:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, "accounts/verify_otp.html", {"email": email})

        # OTP is correct -> create the actual user account now
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            del request.session["register_data"]
            return redirect("accounts:register")

        user = User.objects.create_user(
            username=register_data["username"],
            email=email,
            password=register_data["password"],
        )
        user.phone_number = register_data.get("phone_number", "")
        user.is_verified = True
        user.save()

        # cleanup
        EmailOTP.objects.filter(email=email).delete()
        del request.session["register_data"]

        login(request, user)
        messages.success(request, f"Welcome, {user.username}! Your account has been created.")
        return redirect("home")

    return render(
        request,
        "accounts/verify_otp.html",
        {"email": email}
    )


def resend_otp(request):

    register_data = request.session.get("register_data")
    reset_email = request.session.get("reset_email")

    if register_data:
        send_otp_email(register_data["email"], purpose="register")
        messages.success(request, "A new OTP has been sent to your email.")
        return redirect("accounts:verify_otp")

    if reset_email:
        send_otp_email(reset_email, purpose="reset")
        messages.success(request, "A new OTP has been sent to your email.")
        return redirect("accounts:forgot_password_verify_otp")

    messages.error(request, "Session expired. Please try again.")
    return redirect("accounts:register")


def forgot_password_view(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, "accounts/forgot_password.html")

        if not User.objects.filter(email__iexact=email).exists():
            messages.error(request, "No account found with this email address.")
            return render(request, "accounts/forgot_password.html")

        request.session["reset_email"] = email
        # a fresh reset request always needs a fresh OTP verification
        request.session["reset_verified"] = False

        send_otp_email(email, purpose="reset")
        messages.success(request, "An OTP has been sent to your email.")

        return redirect("accounts:forgot_password_verify_otp")

    return render(request, "accounts/forgot_password.html")


def forgot_password_verify_otp(request):

    email = request.session.get("reset_email")

    if not email:
        messages.error(request, "Session expired. Please start again.")
        return redirect("accounts:forgot_password")

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        otp_obj = EmailOTP.objects.filter(email=email).order_by("-created_at").first()

        if not otp_obj:
            messages.error(request, "OTP not found. Please request a new one.")
            return redirect("accounts:forgot_password")

        if otp_obj.is_expired():
            messages.error(request, "OTP has expired. Please request a new one.")
            return render(request, "accounts/forgot_password_verify_otp.html", {"email": email})

        if entered_otp != otp_obj.otp:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, "accounts/forgot_password_verify_otp.html", {"email": email})

        # OTP correct
        EmailOTP.objects.filter(email=email).delete()
        request.session["reset_verified"] = True

        return redirect("accounts:reset_password")

    return render(request, "accounts/forgot_password_verify_otp.html", {"email": email})


def reset_password_view(request):

    email = request.session.get("reset_email")
    verified = request.session.get("reset_verified")

    if not email or not verified:
        messages.error(request, "Please verify the OTP before resetting your password.")
        return redirect("accounts:forgot_password")

    user = User.objects.filter(email__iexact=email).first()

    if not user:
        messages.error(request, "Account not found. Please try again.")
        return redirect("accounts:forgot_password")

    if request.method == "POST":

        form = StyledSetPasswordForm(user, request.POST)

        if form.is_valid():
            form.save()

            # cleanup session
            del request.session["reset_email"]
            del request.session["reset_verified"]

            messages.success(request, "Password reset successfully! Please login with your new password.")
            return redirect("accounts:login")
    else:
        form = StyledSetPasswordForm(user)

    return render(request, "accounts/reset_password.html", {"form": form})