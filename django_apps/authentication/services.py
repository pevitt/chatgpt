from utils.exceptions import ChatGptAPIException, ErrorCode
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authtoken.models import Token
from typing import Any, Dict


def create_user(
        *,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str
) -> Profile:
    user = User.objects.create_user(
        username=username,
        email=email.lower(),
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    profile = Profile.objects.create(
        user=user
    )
    return profile


def get_token(user) -> Dict[str, Any]:
    Token.objects.get_or_create(user=user)
    profile = Profile.objects.get(user=user)

    data = {
        'token': user.auth_token.key,
    }

    return data
