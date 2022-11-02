from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
from django.conf import settings


class Folder(models.Model):
    foldername = models.CharField(max_length=50)
    folderdesc = models.CharField(max_length=255)
    folderuser = models.ForeignKey(User,on_delete=models.CASCADE)
class File(models.Model):
    filetitle = models.CharField(max_length=50)
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    file = models.FileField(upload_to="files")
    date = models.DateTimeField(default=datetime.datetime.now)

class upload(models.Model):
    upload=models.FileField(upload_to="media",null = True)

class Img(models.Model):
    filetitle = models.CharField(max_length=50)
    file = models.FileField(upload_to="Img/")