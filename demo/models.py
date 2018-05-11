from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.validators import FileExtensionValidator
import datetime

class Subject(models.Model):
    name = models.CharField(max_length=250,unique=True)

    def __str__ (self):
        return self.name

class Exp(models.Model):
    name = models.CharField(max_length=250)

    def __str__ (self):
        return self.name

class Video(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    faculty = models.CharField(max_length=250)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    video_title = models.ForeignKey(Exp,on_delete=models.CASCADE)
    file_file = models.FileField(default='null',validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    rating = models.IntegerField(default=0,null=True)
    comment = models.CharField(max_length=1000,blank=True)
    redo = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
