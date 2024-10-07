from django.db import models

# Create your models here.
class Photo(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    url = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    format = models.CharField(max_length=16, default='png')
    width = models.IntegerField()
    height = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    url = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    format = models.CharField(max_length=16, default='mp4')
    duration = models.FloatField(null=True) 
    width = models.IntegerField(null=True)   
    height = models.IntegerField(null=True)  
    bit_rate = models.IntegerField(null=True)  
    frame_rate = models.FloatField(null=True)  
    created_at = models.DateTimeField(auto_now_add=True)