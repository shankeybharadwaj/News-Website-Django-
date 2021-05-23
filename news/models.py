from __future__ import unicode_literals
from django.db import models

# Create your models here.

class News(models.Model):
    name = models.CharField(default="-",max_length=200)
    short_txt = models.TextField(default="-")
    body_txt = models.TextField(default="-")
    date = models.CharField(default="-",max_length=12)
    time = models.CharField(default="00:00",max_length=12)
    writer = models.CharField(default="-",max_length=50)
    picname=models.TextField(default="-")
    picurl=models.TextField(default="-")
    catname = models.CharField(default="-",max_length=50)   # subcat name
    catid = models.IntegerField(default=0)  # subcat id
    ocatid = models.IntegerField(default=0) # id of main category
    show = models.IntegerField(default=0)
    tag = models.TextField(default="-")
    act = models.IntegerField(default=0)    # activated or not

    def __str__(self):
        return self.name
         
