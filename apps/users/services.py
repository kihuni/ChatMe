import pyotp
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import CustomUser

class AuthenticationService:
    @staticmethod
    def validate_login_attempts(user):
        """
        Manage login attempts and lockouts
        """
        MAX_ATTEMPTS = 5
        LOCKOUT_DURATION = timezone.timedelta(minutes=15)

        now = timezone.now()
        user.last_login_attempt = now
        user.login_attempts += 1

        if user.login_attempts >= MAX_ATTEMPTS:
            user.is_locked = True
            user.locked_until = now + LOCKOUT_DURATION
            user.save()
            raise ValidationError("Account temporarily locked due to multiple failed attempts")

    @staticmethod
    def generate_mfa_secret():
        """
        Generate Multi-Factor Authentication Secret
        """
        return pyotp.random_base32()

    @staticmethod
    def verify_mfa_token(secret, user_token):
        """
        Verify Multi-Factor Authentication Token
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(user_token)