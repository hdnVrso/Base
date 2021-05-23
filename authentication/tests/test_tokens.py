from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.urls import include, path, reverse
from django.test import TransactionTestCase
from ..models import User


class ObtainTokenTests(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path('api/', include('authentication.urls'))
    ]
    username = 'FakeUser'
    email = 'fake@email.com'
    password = 'Pass1234'

    def setUp(self):
        self.user = User.objects.create_user(
            username=ObtainTokenTests.username,
            email=ObtainTokenTests.email,
            password=ObtainTokenTests.password)

    def test_returns_400_bad_request_if_has_no_email(self):
        url = reverse('authentication:obtain_token')
        request = {'user': {'password': ObtainTokenTests.password}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_has_no_password(self):
        url = reverse('authentication:obtain_token')
        request = {'user': {'email': ObtainTokenTests.email}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_400_bad_request_if_has_incorrect_email(self):
        url = reverse('authentication:obtain_token')

        request = {'user': {'email': 'emailemail.com',
                            'password': ObtainTokenTests.password}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_200_ok_if_request_is_valid(self):
        url = reverse('authentication:obtain_token')

        request = {'user': {'email': ObtainTokenTests.email,
                   'password': ObtainTokenTests.password}}
        response = self.client.post(url, request, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)


class RefreshTokenTests(APITestCase, URLPatternsTestCase, TransactionTestCase):
    urlpatterns = [
        path('api/', include('authentication.urls'))
    ]
    username = 'FakeUser'
    email = 'fake@email.com'
    password = 'Pass1234'

    def setUp(self):
        self.user = User.objects.create_user(
            username=RefreshTokenTests.username,
            email=RefreshTokenTests.email,
            password=RefreshTokenTests.password)

    def test_returns_403_forbidden_if_request_has_no_token(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_403_forbidden_if_request_has_no_token_type_prefix(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_403_forbidden_if_request_has_invalid_token_type_prefix(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_403_forbidden_if_request_has_invalid_token(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_403_forbidden_if_request_has_expired_token(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_200_ok_if_request_is_valid(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_returns_correct_body_if_request_is_valid(self):
        url = reverse('authentication:refresh_token')
        refresh_token = self.user.refresh_token
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)