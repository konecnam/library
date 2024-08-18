from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class UploadedBook(models.Model):
    file_name = models.CharField(max_length=1024)
    file = models.FileField(upload_to='uploads/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1024, null=True)
    author_of_book = models.CharField(max_length=1024, null=True)
    
