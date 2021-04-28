from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.urls import include, path, reverse
from django.test import TransactionTestCase


class RegistrationTests(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path('api/', include('authentication.urls'))
    ]

    def test_returns_400_bad_request_if_request_has_no_email(self):
        url = reverse('authentication:register')
        request = {'password': 'pass1234', 'username': 'user1214'}
        response = self.client.post(url, format='json', request=request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_request_has_no_password(self):
        url = reverse('authentication:register')
        request = {'email': 'email@email.com', 'username': 'user1214'}
        response = self.client.post(url, format='json', request=request)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_request_has_no_username(self):
        url = reverse('authentication:register')
        request = {'email': 'email@email.com', 'password': 'pass1234'}
        response = self.client.post(url, format='json', request=request)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_email_has_wrong_format(self):
        url = reverse('authentication:register')
        request = {'email': 'emailemail.com', 'username': 'user1214', 'password': 'Pass1234'}
        response = self.client.post(url, format='json', request=request)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_200_ok_if_request_is_valid(self):
        url = reverse('authentication:register')
        request = {'email': 'email@email.com', 'username': 'use1214',
                   'password': 'Pass1234'}
        response = self.client.post(url, format='json', request=request)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_returns_correct_response_body_if_request_is_valid(self):
        url = reverse('authentication:register')
        request = {'email': 'email@email.com', 'username': 'user1214',
                   'password': 'Pass1234'}
        response = self.client.post(url, format='json', request=request)
        self.assertEqual(response.data, {
                             'email': request['email'],
                             'username': request['username']
        })