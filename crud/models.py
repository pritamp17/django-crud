from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
