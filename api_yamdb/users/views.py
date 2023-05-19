from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import SignupSerializer, TokenSerializer

User = get_user_model()


class APISignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save(confirmation_code=str(uuid4()))
        except IntegrityError:
            return Response(
                {'error': 'Такой пользователь уже существует.'},
                status=status.HTTP_400_BAD_REQUEST)
        send_mail(
            subject='Вы зарегистрированы на YamDB',
            message='Вы зарегистрированы на YamDB \n'
            f'Ваше имя пользователя: {user.username} \n'
            f'Ваш код доступа к API: {user.confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APITokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'error': 'Такого пользователя не существует.'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Неверный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST)
