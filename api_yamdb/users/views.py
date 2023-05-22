from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsAdminRole
from users.serializers import (ReadonlyRoleSerializer, SignupSerializer,
                               TokenSerializer, UsersSerializer)

User = get_user_model()


class APISignupView(APIView):

    def post(self, request):
        """
        Эндпоинт для регистрации новых пользователей
        или для получения доступа к данным для получения токена
        """

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save(confirmation_code=str(uuid4()))
        except IntegrityError:
            try:
                user = User.objects.get(
                    username=request.data['username'],
                    email=request.data['email']
                )
            except User.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с этим именем '
                              'или e-mail уже существует'},
                    status=status.HTTP_400_BAD_REQUEST)
        send_mail(
            subject='Ваш код доступа к YamDB',
            message='Ваш данные для доступа к YamDB \n'
            f'Ваше имя пользователя: {user.username} \n'
            f'Ваш код доступа к API: {user.confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APITokenView(APIView):

    def post(self, request):
        """Эндпоинт для получения аутентификационного токена"""

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


class UsersViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для работы с учётными записями пользователей
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def user_detail(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = ReadonlyRoleSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
