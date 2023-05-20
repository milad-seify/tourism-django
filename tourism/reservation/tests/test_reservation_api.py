"""Test for reservation API"""

from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Reservation
from reservation.serializer import ReservationSerializer

RESERVATION_URL = reverse('reservation:reservation-list')


def create_reservation(user, **params):  # helper function
    """Create and return a sample Reservations"""

    defaults = {
        'title': 'test res',
        'detail': 'test det',
        'type': 'hotel',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
    }
    # for override value in default data model of reservation
    defaults.update(params)

    reservation = Reservation.objects.create(user=user, **defaults)
    return reservation


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)  # type: ignore


class PublicReservationTest(TestCase):
    """Test unauthenticated API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        response = self.client.get(RESERVATION_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReservationTest(TestCase):
    """Test Authenticated API requests """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@example.com',
            password='passtestres123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reservation(self):
        """Test retrieving a list of reservation"""
        create_user(user=self.user)
        create_user(user=self.user)

        response = self.client.get(RESERVATION_URL)

        reservation = Reservation.objects.all().order_by('-id')
        serializer = ReservationSerializer(reservation, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)  # type: ignore
