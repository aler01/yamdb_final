from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.utils import generate_confirmation_code

ROLES = (
    ('admin', 'admin'),
    ('user', 'user'),
    ('moderator', 'moderator')
)


class User(AbstractUser):
    """Переопределенный пользователь, подходящий под нужды проекта."""
    bio = models.CharField(
        max_length=3000, null=True,
        verbose_name='Информация о себе'
    )
    confirmation_code = models.CharField(
        max_length=50, null=True,
        verbose_name='Код подтверждения',
        default=generate_confirmation_code()
    )
    role = models.CharField(
        max_length=50, choices=ROLES,
        verbose_name='Роль'
    )
    username = models.CharField(
        max_length=150, unique=True,
        blank=False, null=False
    )
    email = models.EmailField(
        max_length=255, unique=True,
        blank=False, null=False
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
