from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class Role(models.Model):
    ROLE_CHOICES = [
        (1, 'Platform Administrator'),
        (2, 'Room Moderator'),
        (3, 'Regular Member'),
        (4, 'Limited Access User'),
    ]
    
    name = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    
    # User Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # Profile and Role Management
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=3, related_name='users')

    # Account Locking
    _locked_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def lock_account(self, minutes=15):
        """Locks the account temporarily."""
        self._locked_until = timezone.now() + timezone.timedelta(minutes=minutes)
        self.save()

    def is_account_locked(self):
        """Checks if the account is locked."""
        if self._locked_until and timezone.now() < self._locked_until:
            return True
        return False

    def unlock_account(self):
        """Unlocks the account."""
        self._locked_until = None
        self.save()
