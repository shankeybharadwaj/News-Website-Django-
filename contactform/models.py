from __future__ import unicode_literals
from django.db import models

# Create your models here.

class ContactForm(models.Model):
    
    name = models.CharField(default="-",max_length=50)
    email = models.CharField(default="-",max_length=50)
    txt = models.TextField(default="-")
    date = models.CharField(default="",max_length=12) 
    time = models.CharField(default="",max_length=12) 
    
    def __str__(self):
        return self.name
         