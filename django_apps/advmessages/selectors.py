from .models import AdviserMessages, Profile
from django.db.models import QuerySet


def filter_messages_by_profile(
        profile: Profile
) -> 'QuerySet[AdviserMessages]':
    return AdviserMessages.objects.filter(
        profile=profile
    )
