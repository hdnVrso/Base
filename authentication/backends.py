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
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except BaseException:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

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
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms='HS256')
        except BaseException:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        if payload['type'] != 'refresh':
            raise exceptions.AuthenticationFailed('Wrong token type')

        if payload['exp'] < int(datetime.now().strftime('%s')):
            raise exceptions.AuthenticationFailed('Token expired')

        try:
            user = User.objects.get(id=payload.get('id'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
