from django.db import models
from core.models import College

class CG(models.Model):
    
    clg = models.ForeignKey(College, related_name='cg',on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50)
    year = models.IntegerField(default="1")
    deg = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    sd = models.TextField()
    
    jd = models.CharField(max_length=255)
    loc = models.CharField(max_length=50,default="India")
    sal = models.CharField(max_length=10)
    skills = models.TextField()
    duration = models.CharField(max_length=100,default="4")
    
    
    output = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    
    