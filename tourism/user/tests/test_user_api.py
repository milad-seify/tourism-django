"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')  # this url for update or see information of user


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)  # type: ignore


class PublicUserApiTests(TestCase):
    """Test the public features of the user API.before users auth themselves"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'testpass123',
            'phone_number': '09145632578',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)  # type: ignore

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'testpass123',
            'phone_number': '09145672578',

        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'pw',
            'phone_number': '09145636578',

        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

        # """Token User Testing """

    def test_create_token_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'first_name': 'test',
            'last_name': 'test',
            'password': 'testpassword@123',
            'email': 'user@example.com',
            'phone_number': '09175632578',

        }

        create_user(**user_details)

        payload = {
            'password': user_details['password'],
            'email': user_details['email'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)  # type: ignore
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """Test returns error if credential invalid"""
        create_user(email='test@example.com', password='truepassword')

        payload = {'email': 'test@example.com', 'password': 'falsepassword'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)  # type: ignore
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {'email': 'test@example.com', 'password': ''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)  # type: ignore
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test Api request that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            first_name='test',
            last_name='test',
            password='passwordtest123',
            phone_number=6145637578

        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.user.email)  # type: ignore
        self.assertEqual(res.data['first_name'],  # type: ignore
                         self.user.first_name)

    def test_http_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user"""
        payload = {'first_name': 'updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # image test user api.


# class ImageUploadTests(TestCase):
#     """Test for the image upload API."""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(  # type: ignore
#             email='test@example.com',
#             password='usertest123pass',
#         )
#         self.client.force_authenticate(self.user)
#         self.recipe = create_recipe(user=self.user)

#     def tearDown(self):
#         self.recipe.image.delete()

#     def test_uploads_image(self):
#         """Test uploading an image to a user."""
#         url = image_upload_url(self.recipe.id)  # type: ignore
#         with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
#             img = Image.new('RGB', (10, 10))
#             img.save(image_file, format='JPEG')
#             image_file.seek(0)
#             payload = {'image': image_file}
#             response = self.client.post(url, payload, format='multipart')

#         self.recipe.refresh_from_db()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('image', response.data)  # type: ignore
#         self.assertTrue(os.path.exists(self.recipe.image.path))

#     def test_upload_image_bad_request(self):
#         """Test uploading invalid image."""
#         url = image_upload_url(self.recipe.id)  # type: ignore
#         payload = {'image': 'notanimage'}
#         response = self.client.post(url, payload, format='multipart')

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
