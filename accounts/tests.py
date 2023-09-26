from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.serializers import AccountRegisterSerializer


class AccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'password': 'password123'
        }
        self.login_data = {
            'phone': self.user_data['phone'],
            'password': self.user_data['password']
        }
        account = AccountRegisterSerializer(data=self.user_data)
        if account.is_valid():
            account.save()

    def test_register_successful(self):
        user_data = {
            **self.user_data,
            'phone': '9876543210'
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_register_phone_already_exists(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['phone'][0], 'account with this phone already exists.')

    def test_login_successful(self):
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_password(self):
        invalid_data = {
            'phone': self.user_data['phone'],
            'password': 'wrong_password'
        }
        response = self.client.post(self.login_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid password')

    def test_login_account_not_found(self):
        non_existent_phone = '9876543210'
        invalid_data = {
            'phone': non_existent_phone,
            'password': 'password123'
        }
        response = self.client.post(self.login_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Account not found')

