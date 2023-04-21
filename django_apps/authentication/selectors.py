# Django
from django.db.models import QuerySet
from typing import Any
# Models
from .models import Profile
from django.contrib.auth.models import User


def filter_user_by_email(
        *,
        email: str
) -> 'QuerySet[User]':
    return User.objects.filter(
        email=email
    )


def filter_user_by_names(
        *,
        first_name: str,
        last_name: str
) -> 'QuerySet[User]':
    return User.objects.filter(
        first_name=first_name,
        last_name=last_name
    )


def filter_profile_by_user(
        *,
        user: User
) -> 'QuerySet[Profile]':
    return Profile.objects.filter(
        user=user
    )
