
from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

class User(AbstractUser):
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        max_length=150,
        unique=True)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=True)
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        blank=True)
    email = models.EmailField(
        'e-mail',
        max_length=254,
        unique=True)
    bio = models.TextField(
        'Биография',
        blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=ROLE_CHOICES,
        default=USER)
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True)

    def __str__(self) -> str:
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
