import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, purpose="register"):

    # Purana OTP delete
    EmailOTP.objects.filter(email=email).delete()

    otp = generate_otp()

    EmailOTP.objects.create(
        email=email,
        otp=otp
    )

    if purpose == "reset":
        subject = "DriveEasy Password Reset OTP"
        intro = "You requested to reset your DriveEasy account password."
    else:
        subject = "DriveEasy Email Verification"
        intro = "Welcome to DriveEasy Car Rental."

    message = f"""
Hello,

{intro}

Your OTP is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank You,
DriveEasy Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )