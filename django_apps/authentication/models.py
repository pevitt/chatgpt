from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE)
    bio = models.TextField(
        null=True,
        blank=True)
    skills = models.CharField(
        max_length=1000,
        null=True,
        blank=True)

    def __str__(self):
        return self.user.email
