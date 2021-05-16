from django.contrib.auth.models import User
from django.db import models


class RequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, max_length=100)
    timestamp = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.text
