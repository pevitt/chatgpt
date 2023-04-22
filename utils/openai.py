import os
import openai
from django.conf import settings


class AdvMessagesService:

    def __init__(self):
        openai.api_key = settings.OPENAI_KEY

    def set_messages_openai(self, messages):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response
