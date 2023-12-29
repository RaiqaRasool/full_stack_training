from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to="profile_avatars/", blank=True, null=True)
