from django.utils import timezone
from django.db import models
from authentication.models import User


class RequestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
