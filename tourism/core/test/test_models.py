""""  test for models ."""
from decimal import Decimal
from unittest.mock import patch
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='test@example.com', password='testuser123',
                first_name='testuser',
                last_name='testuserlastname', phone_number=69156987845):
    """Create and return new user"""
    return get_user_model().objects.\
        create_user(email=email, password=password,  # type: ignore
                    first_name=first_name,\
                    last_name=last_name, phone_number=phone_number)


def create_reservation(user, title='testtitle',
                       detail='detailtest', type='test',
                       created_at=datetime.now(), updated_at=datetime.now()):
    """Create and return reservation"""
    return models.Reservation.objects.create(user=user, title=title,
                                             detail=detail,
                                             type=type, created_at=created_at,
                                             updated_at=updated_at)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        first_name = 'testuser'
        last_name = 'testuserlastname'
        phone_number = 65987485112
        user = get_user_model().objects.create_user(  # type: ignore
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        i = 0
        for email, expected in sample_emails:
            i += 1
            phon_gen = 3659854231 + i
            user = get_user_model()\
                .objects.\
                create_user(email, 'sample123',  # type: ignore
                            phone_number=phon_gen)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(  # type: ignore
                '', 'pass123',)

    def test_create_superuser(self):
        """test that creating a superuser"""
        user = get_user_model().objects.create_superuser(  # type: ignore
            'test@test.com',
            'pass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_comments(self):
        """Test creating a comment is successful."""
        user = create_user()
        comment = models.Comment.objects.create(
            user=user,
            feedback='That`s a comment',
            created_at=datetime.now(),
        )
        self.assertEqual(str(comment), comment.feedback)

    def test_create_reservation(self):
        """Test creating a reservation is successful"""
        user = get_user_model().objects.create_user(  # type: ignore
            email='reservation@example.com',
            password='resrtestpass12',
            phone_number=65987485112,
        )
        reservation = models.Reservation.objects.create(
            title='res test',
            detail='some thing detail test',
            type='type test',
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user=user,
            # TODO:Maybe add image field
        )
        self.assertEqual(str(reservation), reservation.title)

    def test_create_hotel_and_residence(self):
        """Test creating a Hotel and Residence is successful"""

        user = get_user_model().objects.create_user(  # type: ignore
            email='hotelandre@example.com',
            password='resrtestpass12',
            phone_number=659874846912
        )
        reservation = create_reservation(user=user)
        hotel_and_residence = models.HotelAndResidence.objects.create(
            reservation=reservation,
            name='testhote',
            type_hotel='asfs',
            address='testaddresshotel',
            facilities='testfacilitieshotel',
            cost=Decimal(1.00),
        )
        self.assertEqual(str(hotel_and_residence), hotel_and_residence.name)

    def test_tourist_tour(self):
        """Test creating a Tourist Tours is successful"""

        user = create_user()
        reservation = create_reservation(user=user)
        tourist = models.TouristTour.objects.create(
            name='testnametour',
            facilities='testfacalities',
            description='testdescription',
            cost=Decimal(1.00),
            reservation=reservation
        )
        self.assertEqual(str(tourist), tourist.name)

    def test_travel_agency(self):
        """Test creating a Travel Agency is successful"""
        user = create_user()
        reservation = create_reservation(user=user)
        travel = models.TravelAgency.objects.create(
            name='testagency',
            phone_number=91141751114,
            cost=Decimal(1.00),
            reservation=reservation
        )
        self.assertEqual(str(travel), travel.name)
    # ensure we that we don't have or create any duplicate file name in system.

    @patch('core.models.uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(  # type: ignore
            None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/user/{uuid}.jpg')
