from utils.exceptions import ChatGptAPIException, ErrorCode
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authtoken.models import Token
from typing import Any, Dict
from . import selectors as users_selectors
from django.db.models import F
from advmessages import services as messages_services


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


def filter_profile_by_user(user) -> Dict[str, Any]:
    profile_qry = users_selectors.filter_profile_by_user(
        user=user
    ).annotate(
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email')
    ).values(
        'email',
        'first_name',
        'last_name',
        'bio',
        'skills'
    )
    data = profile_qry.first()

    return data


def update_profile_user(
        *,
        bio: str,
        skills: str,
        user: User
) -> Dict[str, Any]:
    profile_qry = users_selectors.filter_profile_by_user(
        user=user
    ).first()

    profile_qry.bio = bio
    profile_qry.skills = skills
    profile_qry.save()


    message = messages_services.create_message_system(profile_qry)

    profile_qry = users_selectors.filter_profile_by_user(
        user=user
    ).annotate(
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email')
    ).values(
        'email',
        'first_name',
        'last_name',
        'bio',
        'skills'
    )
    data = profile_qry.first()

    return data
