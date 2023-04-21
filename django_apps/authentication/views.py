from django.shortcuts import render
from rest_framework import permissions
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import selectors as users_selectors
from . import services as users_services
from utils.exceptions import ChatGptAPIException, ErrorCode
from .backends import EmailAuthBackend


# Create your views here.
class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(
            max_length=100
        )
        last_name = serializers.CharField(
            max_length=100
        )
        password = serializers.CharField()

        def validate_email(self, data):
            email = data.lower()
            user = users_selectors.filter_user_by_email(
                email=email
            )
            if user.exists():
                raise ChatGptAPIException(ErrorCode.C01)
            return email

        def validate(self, data):
            first_name = data['first_name']

            last_name = data['last_name']
            username = '%s.%s' % (first_name.lower(), last_name.lower())
            username = '{:.29}'.format(username)

            counter = users_selectors.filter_user_by_names(
                first_name=first_name,
                last_name=last_name
            ).count()

            if counter > 0:
                username += '%s' % (counter + 1)
            data['username'] = username
            return data

    def post(self, request):
        in_serializer = self.InputSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)

        try:
            data = users_services.create_user(
                **in_serializer.validated_data
            )
        except:
            raise ChatGptAPIException(ErrorCode.E00)

        return Response(
            data={},
            status=status.HTTP_201_CREATED
        )


class LoginApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=100)
        password = serializers.CharField(max_length=150)

        def validate(self, data):
            email = data.get('email').lower()
            password = data.get('password')
            backend = EmailAuthBackend()
            if email and password:
                user = backend.authenticate(email=email, password=password)
                if user:
                    if not user.is_active:
                        raise ChatGptAPIException(ErrorCode.C02)
                else:
                    raise ChatGptAPIException(ErrorCode.C03)
            else:
                raise ChatGptAPIException(ErrorCode.C04)

            data['user'] = user
            return data

    def post(self, request):
        serializer_data = self.InputSerializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        user = serializer_data.validated_data['user']
        data = {}
        try:
            data = users_services.get_token(user)
        except:
            raise ChatGptAPIException(ErrorCode.E00)

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
