from django.db import models
from core.models import College

class CoursePlan(models.Model):
    clg = models.ForeignKey(College,on_delete=models.CASCADE)
    
    name=models.CharField(max_length=255)    
    major=models.CharField(max_length=255)    
    branch=models.CharField(max_length=255)    
    sbranch=models.CharField(max_length=255)    
    subject=models.CharField(max_length=255)    
    syllbus=models.TextField()
    tp = models.CharField(max_length=50,default="45")
    pd = models.CharField(max_length=50,default="50")
    
    output = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    