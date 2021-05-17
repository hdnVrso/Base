from django.db import models


class ResetPwModel(models.Model):
    userMail = models.TextField(blank=False, max_length=100)
    token = models.TextField(blank=False, max_length=100)

    def __str__(self):
        return self.userMail
