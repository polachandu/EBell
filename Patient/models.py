from django.db import models


# Create your models here.
class Bell(models.Model):
    message = models.CharField(max_length=120)
    priority = models.IntegerField(default=1)
    staff = models.CharField(max_length=10)
    emergency = models.CharField(max_length=5)
    room_number = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
