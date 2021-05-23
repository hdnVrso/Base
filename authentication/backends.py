from datetime import datetime

from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions

import jwt

from .models import User


class JWTAccessAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(
            request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            raise exceptions.AuthenticationFailed('No auth header')

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('No token given')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid auth header')

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            raise exceptions.AuthenticationFailed('Invalid token type prefix')

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except BaseException:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        if payload['type'] != 'access':
            raise exceptions.AuthenticationFailed('Wrong token type')

        if payload['exp'] < datetime.now():
            raise exceptions.AuthenticationFailed('Token expired')

        try:
            user = User.objects.get(id=payload.get('id'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None


class JWTRefreshAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(
            request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            raise exceptions.AuthenticationFailed('No auth header')

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('No token given')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid auth header')

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            raise exceptions.AuthenticationFailed('Invalid token type prefix')

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms='HS256')
        except BaseException:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        if payload['type'] != 'refresh':
            raise exceptions.AuthenticationFailed('Wrong token type')

        if payload['exp'] < int(datetime.now().strftime('%s')):
            raise exceptions.AuthenticationFailed('Token expired')

        try:
            user = User.objects.get(id=payload.get('id'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
