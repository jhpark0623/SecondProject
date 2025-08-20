from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True )
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.username
