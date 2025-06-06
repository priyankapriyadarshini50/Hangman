from django.db import models
from django.contrib.auth.models import AbstractUser
from game.models import Game
from users.manager import GameUserManager

# Create your models here.
class GameUsers(AbstractUser):

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = GameUserManager()
