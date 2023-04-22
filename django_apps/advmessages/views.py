from django.shortcuts import render
from utils.openai import AdvMessagesService
from . import services as messages_services
from .models import Profile
from utils.exceptions import ChatGptAPIException, ErrorCode

from rest_framework import permissions
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class MessageRequestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    class OutputSerializer(serializers.Serializer):
        message = serializers.CharField()
        role = serializers.CharField()
        created_at = serializers.DateTimeField()

    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()

        messages = messages_services.get_mesages_by_profile_by_role(
            profile=profile,
            role='assistant'
        )

        output_serializer = self.OutputSerializer(
            data=messages,
            many=True
        )

        try:
            output_serializer.is_valid(raise_exception=True)
        except:
            raise ChatGptAPIException(ErrorCode.E00)

        return Response(output_serializer.data)

    def post(self, request):
        profile = Profile.objects.filter(user=request.user).first()

        messages = messages_services.process_message_by_profile(
            profile=profile
        )

        output_serializer = self.OutputSerializer(data=messages.__dict__)

        try:
            output_serializer.is_valid(raise_exception=True)
        except:
            raise ChatGptAPIException(ErrorCode.E00)

        return Response(output_serializer.validated_data)
