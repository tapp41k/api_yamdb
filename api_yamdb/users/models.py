from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь')
    ]
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль на сайте',
        max_length=9,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=36,
        default='confirmation_code_123'
    )
    email = models.EmailField(
        'Адрес e-mail',
        unique=True
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_unprivileged(self):
        return self.role == 'user'
