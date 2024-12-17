import pyotp
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import CustomUser

class AuthenticationService:
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = timezone.timedelta(minutes=15)

    @staticmethod
    def validate_login_attempts(user):
        now = timezone.now()
        user.last_login_attempt = now
        user.login_attempts += 1

        if user.login_attempts >= AuthenticationService.MAX_ATTEMPTS:
            user.lock_account(minutes=15)
            raise ValidationError("Account temporarily locked due to multiple failed attempts")

    @staticmethod
    def generate_mfa_secret():
        return pyotp.random_base32()

    @staticmethod
    def verify_mfa_token(secret, user_token):
        totp = pyotp.TOTP(secret)
        return totp.verify(user_token)
