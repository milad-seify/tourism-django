""""  test for models ."""

from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(  # type: ignore
            email=email,
            password=password,
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
        for email, expected in sample_emails:
            user = get_user_model()\
                .objects.create_user(email, 'sample123')  # type: ignore
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')  # type: ignore

    def test_create_superuser(self):
        """test that creating a superuser"""
        user = get_user_model().objects.create_superuser(  # type: ignore
            'test@test.com',
            'pass123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_reservation(self):
        """Test creating a reservation is successful"""
        user = get_user_model().objects.create_user(  # type: ignore
            email='reservation@example.com',
            password='resrtestpass12',
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
