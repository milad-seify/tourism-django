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


def detail_url(reservation_id):
    """Create and return a reservation detail url"""
    return reverse('reservation:reservation-detail')


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
            password='passtestres123',
            phone_number=4756987456
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

    def test_reservation_list_to_user(self):
        """Test list of reservation is limited authenticated user."""

        unathen_user = create_user(
            email='test@example.com', password='psastest123')

        create_reservation(user=unathen_user)
        create_reservation(user=self.user)

        response = self.client.get(RESERVATION_URL)

        reservation = Reservation.objects.filter(user=self.user)
        serializer = ReservationSerializer(reservation, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)  # type: ignore

        # for access specific item in model with url

    def test_get_reservation_detail(self):
        """Test get reservation detail"""
        reservation = create_reservation(user=self.user)

        url = detail_url(reservation_id=reservation.id)  # type: ignore
        response = self.client.get(url)

        serializer = ReservationSerializer(reservation)
        self.assertEqual(response.data, serializer.data)  # type: ignore

    def test_create_reservation(self):
        """Test creating a reservation"""
        payload = {
            'title': 'test create',
            'detail': 'test det',
            'type': 'tourism',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }
        response = self.client.post(RESERVATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservation = Reservation.objects.get(
            id=response.data['id'])  # type: ignore

        for v, k in payload.items():
            self.assertEqual(getattr(reservation, k), v)
        self.assertEqual(reservation.user, self.user)

    def test_partial_update(self):
        """Test partial update of a reservation"""

        original_type = 'hotel'
        reservation = create_reservation(
            user=self.user,
            title='HELLO',
            type=original_type,
        )
        payload = {'title': 'new hello'}
        url = detail_url(reservation_id=reservation.id)  # type: ignore
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation.refresh_from_db()
        self.assertEqual(reservation.title, payload['title'])
        self.assertEqual(reservation.type, original_type)
        self.assertEqual(reservation.user, self.user)

    def test_full_update(self):
        """Test full update of reservation"""
        reservation = create_reservation(
            user=self.user,
            title='test ti',
            detail='test det',
            type='hotel',
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        payload = {
            'title': 'newt create',
            'detail': 'newt det',
            'type': 'agency',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }

        url = detail_url(reservation_id=reservation.id)  # type: ignore
        response = self.client.put(url, payload)

        self.assertEqual(response, status.HTTP_200_OK)
        reservation.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(reservation, k), v)
        self.assertEqual(reservation.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the reservation user results in an error"""
        new_user = create_user(email='newtest@example.com',
                               password='newpasstest123')

        reservation = create_reservation(user=new_user)

        payload = {'user': new_user.id}

        url = detail_url(reservation_id=reservation.id)  # type: ignore
        self.client.patch(url, payload)
        # TODO:check here !
        # i thin should not be equal!
        reservation.refresh_from_db()
        self.assertEqual(reservation.user, self.user)

    def test_delete_reservation(self):
        """Test deleting a reservation successful"""
        reservation = create_reservation(user=self.user)

        url = detail_url(reservation_id=reservation.id)  # type: ignore
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(
            id=Reservation.id).exists())  # type: ignore

    def test_delete_other_users_reservation_error(self):
        """Test trying to delete another users reservation,gives error"""

        new_user = create_user(
            email='newuser@example.com', password='passnew123')

        reservation = create_reservation(user=new_user)

        url = detail_url(reservation_id=reservation.id)  # type: ignore
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Reservation.objects.filter(
            id=reservation.id).exists())  # type: ignore
