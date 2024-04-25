from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    update = models.DateTimeField(auto_now=True, blank=True)
    complated = models.BooleanField(default=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.task
    

class Movie(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    rating = models.IntegerField()

    uzb_gross = models.IntegerField()
    world_gross = models.IntegerField()
    phone_number = models.CharField(max_length=13)

    def __str__(self) -> str:
        return self.title
    