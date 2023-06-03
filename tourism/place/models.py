import os


from django.conf import settings
from django.db import models
from django.contrib.gis.db import models
import uuid
from django.core.validators import (
    FileExtensionValidator)
from core.models import User


def places_image_file_path(instance, filename):
    """Generate file path for new user image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'places', filename)


class Places(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=300)
    TYPE_PLACES = (
        ('RECREATIONAL', 'RECREATIONAL'),
        ('SHOPPING', 'SHOPPING'),
        ('TOURISM', 'TOURISM')
    )
    type = models.CharField(
        max_length=13, choices=TYPE_PLACES, default='NOTSET')

    # DEFAULT_ADMIN_ID = User.objects.filter(is_superuser=True).first().id or 0
    # if DEFAULT_ADMIN_ID is None:
    #     DEFAULT_ADMIN_ID = 0

    admin_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.name
    # class Meta:
    #     permission_required = True
    #     permissions = [
    #         ("change_places", "Can edit the places"),
    #     ]

    # @permission_required('core.change_places', raise_exception=True)
    # def save(self, *args, **kwargs):
    #     # Only allow users with 'change_mymodel' permission to modify this object
    #     super().save(*args, **kwargs)


class RecreationalPlace(models.Model):
    location = models.PointField()
    image = models.ImageField(upload_to=places_image_file_path, validators=[
                              FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png',])])
    place_id = models.ForeignKey('Places', on_delete=models.CASCADE)


class ShoppingPlace(models.Model):
    location = models.PointField(unique=True)
    image = models.ImageField(upload_to=places_image_file_path, validators=[
                              FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png',])])
    place_id = models.ForeignKey('Places', on_delete=models.CASCADE)


class TourismPlace(models.Model):
    location = models.PointField(unique=True)
    image = models.ImageField(upload_to=places_image_file_path, validators=[
                              FileExtensionValidator(['jpg', 'jpeg', 'gif', 'png',])])
    place_id = models.ForeignKey('Places', on_delete=models.CASCADE)
