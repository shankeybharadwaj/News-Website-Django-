from __future__ import unicode_literals
from django.db import models

# Create your models here.

class SubCat(models.Model):
    
    name = models.CharField(default="-",max_length=50)  # subcat name
    catname = models.CharField(default="-",max_length=50)   # main cat name
    catid = models.IntegerField(default=0)  # pk of main cat
    
    def __str__(self):
        return self.name
         
