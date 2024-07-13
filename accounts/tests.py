from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User


class UserRegistrationTest(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'email': 'phllpsnt72@gmail.com',
            'username': 'testuser',
            'password': 'Testpass@123'
        }

    def test_user_can_register(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])

    def test_user_cannot_register_with_short_password(self):
        self.user_data['password'] = '123'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_with_invalid_username(self):
        self.user_data['username'] = 'test user'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_with_existing_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_cannot_register_without_email(self):
        self.user_data.pop('email')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_without_username(self):
        self.user_data.pop('username')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_register_without_password(self):
        self.user_data.pop('password')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
