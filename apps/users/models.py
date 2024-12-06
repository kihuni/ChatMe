from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class Role(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Platform Administrator'),
        ('moderator', 'Room Moderator'),
        ('member', 'Regular Member'),
        ('guest', 'Limited Access User')
    )

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_name_display()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    
    # User Status and Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Profile and Role Management
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True
    )
    role = models.ForeignKey(
        Role, 
        on_delete=models.SET_DEFAULT, 
        default=None, 
        null=True, 
        related_name='users'
    )

    # Authentication Tracking
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Custom permission logic
        if self.is_superuser or self.is_staff:
            return True
        return super().has_perm(perm, obj)

    def can_create_room(self):
        """
        Role-based room creation permission
        """
        return self.role.name in ['admin', 'moderator']