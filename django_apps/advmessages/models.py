from django.db import models
from authentication.models import Profile


# Create your models here.
class BaseModel(models.Model):
    """
    Abstract class to help models.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated at'
    )

    class Meta:
        abstract = True


class AdviserMessages(BaseModel):
    ROLE = (
        ('system', 'System'),
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )
    profile = models.ForeignKey(
        Profile,
        related_name='profile',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    role = models.CharField(
        max_length=20,
        choices=ROLE
    )
    response = models.JSONField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.message
