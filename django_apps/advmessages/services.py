from .models import AdviserMessages
from . import selectors as messagess_selectors
from .models import Profile
from django.db.models import F
import json
from typing import Any, Dict, List, Optional, Tuple, Union
from utils.openai import AdvMessagesService


def get_mesages_by_profile(
        profile: Profile
) -> Dict[str, Any]:
    messages = messagess_selectors.filter_messages_by_profile(
        profile=profile
    ).order_by(
        'id'
    ).annotate(
        content=F('message')
    ).values(
        'role',
        'content'
    )

    return list(messages)


def get_mesages_by_profile_by_role(
        profile: Profile,
        role: str
) -> Dict[str, Any]:

    messages = messagess_selectors.filter_messages_by_profile(
        profile=profile
    ).filter(
        role=role
    ).order_by(
        'id'
    ).values(
        'message',
        'role',
        'created_at'
    )

    return list(messages)


def process_message_by_profile(
        profile=Profile
) -> Dict[str, any]:

    # import pdb; pdb.set_trace()

    message_service = AdvMessagesService()
    message_user = create_message_user(profile)
    messages = get_messages(profile)
    response = message_service.set_messages_openai(messages)

    return create_message_assistant(profile, response)


def create_message_assistant(profile: Profile, response: any):
    message_response = response['choices'][0]['message']['content']

    message = create_message_ia(
        profile=profile,
        role='assistant',
        message=message_response,
        response=response
    )

    message.save()

    return message


def create_message_system(profile: Profile):
    message_value = 'Eres una IA que ayuda a los desarrolaldores a conseguir trabajo, mi perfil' \
                    ' es el siguiente, {} y mis skills {}'.format(profile.bio, profile.skills)
    try:
        message = AdviserMessages.objects.get(profile=profile, role='system')
        message.message = message_value
        message.save()
    except AdviserMessages.DoesNotExist:
        message = create_message_ia(
            profile=profile,
            role='system',
            message=message_value
        )
    message.save()

    return message


def create_message_user(profile: Profile):
    message_value = ''
    messages_count = messagess_selectors.filter_messages_by_profile(
        profile=profile
    ).count()

    if messages_count > 2:
        message_value = 'Me puedes dar otro  consejo diferente al anterior?'
    else:
        message_value = 'Me puedes dar un consejo para conseguir trabajo con mi perfil'

    message = create_message_ia(
        profile=profile,
        role='user',
        message=message_value
    )
    message.save()
    return message


def get_messages(profile: Profile):
    messages_data = get_mesages_by_profile(
        profile=profile
    )

    return messages_data


def create_message_ia(
        *,
        profile: Profile,
        role: str,
        message: str,
        response: json = None
) -> AdviserMessages:
    return AdviserMessages.objects.create(
        profile=profile,
        role=role,
        message=message,
        response=response
    )
