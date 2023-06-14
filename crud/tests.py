from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import UserModel

class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.name = 'Test User'
        self.email = 'test@example.com'
        self.password = 'testpassword'
        self.bio = 'test bio.'
        self.profile_picture = 'profile_picture.jpg'

    def test_signup_success(self):
        data = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'bio': self.bio,
            'profile_picture': self.profile_picture
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Cool! Sign up successful, Now you can login')

    def test_signup_failure_existing_email(self):
        UserModel.objects.create(name=self.name, email=self.email, password=self.password)
        data = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'bio': self.bio,
            'profile_picture': self.profile_picture
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email already exists')

    def test_signup_failure_missing_fields(self):
        data = {
            'name': self.name,
            'email': self.email,
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Please provide name, email, and password')

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.email = 'test@example.com'
        self.password = 'testpassword'
        UserModel.objects.create(name='Test User', email=self.email, password=self.password)

    def test_login_success(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('Welcome', response.data)

    def test_login_failure_invalid_credentials(self):
        data = {
            'email': self.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid email or password')

class UpdateProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.update_url = reverse('update')
        self.email = 'test@example.com'
        self.password = 'testpassword'
        self.user = UserModel.objects.create(name='Test User', email=self.email, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_update_profile_success(self):
        data = {
            'name': 'Updated User',
            'bio': 'Updated bio'
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully')
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data['name'])
        self.assertEqual(self.user.bio, data['bio'])

    def test_update_profile_failure_invalid_data(self):
        data = {
            'email': 'newemail@example.com'
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.delete_url = reverse('delete')
        self.admin_user = UserModel.objects.create(name='Admin', email='admin@example.com', password='adminpassword')
        self.user = UserModel.objects.create(name='Test User', email='test@example.com', password='testpassword')

    def test_delete_profile_success(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'email': self.user.email
        }
        response = self.client.delete(self.delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User profile deleted successfully')
        self.assertFalse(UserModel.objects.filter(email=self.user.email).exists())

    def test_delete_profile_failure_unauthorized(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'email': self.user.email
        }
        response = self.client.delete(self.delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_profile_failure_invalid_email(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'email': 'invalid@example.com'
        }
        response = self.client.delete(self.delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_profile_failure_server_error(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'email': self.user.email
        }
        with self.assertRaises(Exception):
            response = self.client.delete(self.delete_url, data)

