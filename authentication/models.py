import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('User must have a username.')

        if email is None:
            raise TypeError('User must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superuser must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255,
                                unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # deleted_at
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def access_token(self):
        return self._generate_jwt_access_token()

    @property
    def refresh_token(self):
        return self._generate_jwt_refresh_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_access_token(self):
        dt = datetime.now() + timedelta(days=1)

        access_token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s')),
            'type': 'access',
        }, settings.SECRET_KEY, algorithm='HS256')

        return access_token

    def _generate_jwt_refresh_token(self):
        dt = datetime.now() + timedelta(days=1)

        refresh_token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s')),
            'type': 'refresh',
        }, settings.SECRET_KEY, algorithm='HS256')

        return refresh_token


class RequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, max_length=100)
    timestamp = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.text
