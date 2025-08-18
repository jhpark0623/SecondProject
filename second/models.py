from django.db import models

# Create your models here.
class Violation(models.Model):
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address