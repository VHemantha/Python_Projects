from email.policy import default
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class posts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length = 1024)
    time = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField()

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    like = models.IntegerField()

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.CharField(max_length=524)