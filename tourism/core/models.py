"""
Database models
"""
import uuid
import os


from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.validators import RegexValidator


def user_image_file_path(instance, filename):
    """Generate file path for new user image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'user', filename)


class UserManager(BaseUserManager):
    """manager for users."""

    def create_user(self, email, password=None, **extra_Field):
        """create , save and return new user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_Field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and return new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# lets us explicitly set upload path and filename
# def upload_to(instance, filename):
#     return 'images/{filename}'.format(filename=filename)


class User(AbstractBaseUser, PermissionsMixin):
    """user in the system"""
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default='')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
              message="Phone number must be entered \
                in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17,
        blank=True, default='')  # Validators should be a list
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    card_info = models.CharField(max_length=50, default='')
    image = models.ImageField(null=True, upload_to=user_image_file_path)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Reservation(models.Model):
    title = models.CharField(max_length=12)
    detail = models.TextField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
