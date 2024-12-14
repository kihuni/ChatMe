from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .models import Role

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        
        email = self.normalize_email(email)
        role = extra_fields.pop('role', None) or Role.objects.get(name='member')
        
        user = self.model(
            email=email, 
            username=username, 
            full_name=full_name, 
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email, 
            username, 
            full_name, 
            password, 
            **extra_fields
        )