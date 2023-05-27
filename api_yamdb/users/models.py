from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    ]
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль на сайте',
        max_length=32,
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=36,
    )
    email = models.EmailField(
        'Адрес e-mail',
        unique=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_unprivileged(self):
        return self.role == self.USER
