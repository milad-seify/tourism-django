"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.core.validators import (
    MaxValueValidator, MinValueValidator, FileExtensionValidator)
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.validators import RegexValidator

# from django.contrib.gis.geos import Point


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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default='')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
              message="Phone number must be entered \
                in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17,
        unique=True)  # Validators should be a list
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    card_info = models.CharField(max_length=50, default='')
    image = models.ImageField(
        upload_to=user_image_file_path,  blank=True, default='default.jpeg',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png',])])
    first_time_login = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

# TODO:async


class Comment(models.Model):
    feedback = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.feedback


class Reservation(models.Model):
    title = models.CharField(max_length=12)
    detail = models.TextField(max_length=220, null=True, blank=True)
    RESERVATION_TYPE = (
        ('HOTEL_AND_RESIDENCE', 'HOTEL_AND_RESIDENCE'),
        ('TRAVEL_AGENCY', 'TRAVEL_AGENCY'),
        ('TOURIST_TOUR', 'TOURIST_TOUR')
    )
    type = models.CharField(
        max_length=20, choices=RESERVATION_TYPE, default='NOTSET')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class HotelAndResidence(models.Model):
    name = models.CharField(max_length=50)

    Ho = (
        ('HOTEL', 'HOTEL'),
        ('RESIDENCE', 'RESIDENCE'),
        ('NOTSET', 'NOTSET')
    )
    type_hotel = models.CharField(max_length=10, choices=Ho,
                                  default="NOTSET", db_index=True)
    address = models.CharField(max_length=100)
    facilities = models.TextField(max_length=500)
    star = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    cost = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Cost per night')
    reservation = models.ForeignKey(
        'Reservation', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class TouristTour(models.Model):
    name = models.CharField(max_length=50)
    facilities = models.TextField(max_length=500)
    description = models.TextField(max_length=500, null=True, blank=True)

    BOAT = 'boat'
    CAR = 'car'
    MOTORCYCLE = 'motorcycle'
    To = (
        (BOAT, 'BOAT'),
        (CAR, 'CAR'),
        (MOTORCYCLE, 'MOTORCYCLE')
    )
    type_of_transportation = models.CharField(max_length=11, choices=To,
                                              default=CAR, db_index=True)
    cost = models.DecimalField(
        max_digits=5, decimal_places=2)
    reservation = models.ForeignKey(
        'Reservation',  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TravelAgency(models.Model):
    name = models.CharField(max_length=50)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
              message="Phone number must be entered \
                in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17,
        blank=True, default='')

    BUS = 'bus'
    TRAIN = 'train'
    AIRPLANE = 'airplane'
    SHIP = 'ship'
    NOTSET = 'notset'

    TRA = (
        (BUS, 'BUS'),
        (TRAIN, 'TRAIN'),
        (AIRPLANE, 'AIRPLANE'),
        (SHIP, 'SHIP'),
        (NOTSET, 'NOTSET')
    )
    type_of_transportation = models.CharField(max_length=11, choices=TRA,
                                              default=NOTSET, db_index=True)
    cost = models.DecimalField(
        max_digits=5, decimal_places=2)
    reservation = models.ForeignKey(
        'Reservation',  on_delete=models.CASCADE)

    def __str__(self):
        return self.name
