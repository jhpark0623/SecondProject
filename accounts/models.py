from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True )
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Suggestion(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SuggestionReply(models.Model):
    suggestion = models.OneToOneField(Suggestion, on_delete=models.CASCADE, related_name='reply')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.suggestion.title}"