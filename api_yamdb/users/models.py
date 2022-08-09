from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'Пользователь'
    MODERATOR = 'Модератор'
    ADMIN = 'Администратор'

    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
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
