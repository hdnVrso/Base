import jwt
from django.conf import settings
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.urls import include, path, reverse
from django.test import TransactionTestCase
from ..models import User
from faker import Faker


class ObtainTokenTests(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path('api/', include('authentication.urls'))
    ]

    def setUp(self):
        self.fake = Faker()
        self.user = User.objects.create_user(
            username=self.fake.name(),
            email=self.fake.email(),
            password=self.fake.password()
        )

    def test_returns_400_bad_request_if_has_no_email(self):
        url = reverse('authentication:obtain_token')
        request = {'user': {'password': self.user.password}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_has_no_password(self):
        url = reverse('authentication:obtain_token')
        request = {'user': {'email': self.user.email}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_has_incorrect_email(self):
        url = reverse('authentication:obtain_token')

        request = {'user': {'email': 'emailemail.com',
                            'password': self.user.password}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_200_ok_if_request_is_valid(self):
        url = reverse('authentication:obtain_token')

        request = {'user': {'email': self.user.email,
                   'password': self.user.password}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)


class RefreshTokenTests(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path('api/', include('authentication.urls'))
    ]

    def setUp(self):
        self.fake = Faker()
        self.user = User.objects.create_user(
            username=self.fake.name(),
            email=self.fake.email(),
            password=self.fake.password()
        )

    def test_returns_403_forbidden_if_request_has_no_token(self):
        url = reverse('authentication:refresh_token')
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_returns_403_forbidden_if_request_has_no_token_type_prefix(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        self.client.credentials(HTTP_AUTHORIZATION=refresh_token)
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_returns_403_forbidden_if_request_has_invalid_token_type_prefix(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        self.client.credentials(HTTP_AUTHORIZATION='Invalid_prefix ' + refresh_token)
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_returns_403_forbidden_if_request_has_invalid_token(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + refresh_token + 'some_invalid_string')
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_returns_403_forbidden_if_request_has_expired_token(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token

        # TODO: expire token
        payload = jwt.decode(refresh_token, settings.SECRET_KEY,
                             algorithms='HS256')
        self.client.credentials(
            HTTP_AUTHORIZATION='Invalid_prefix' + refresh_token)
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_returns_200_ok_if_request_is_valid(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + refresh_token)
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_returns_correct_body_if_request_is_valid(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + refresh_token)
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertContains(response, 'access_token')
        self.assertContains(response, 'refresh_token')