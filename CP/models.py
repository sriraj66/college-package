from django.db import models
from utils.models import User

class CoursePlan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    sbranch=models.CharField(max_length=255)    
    subject=models.CharField(max_length=255)    
    syllbus=models.TextField()
    tp = models.CharField(max_length=50,default="45")
    pd = models.CharField(max_length=50,default="50")
    
    output = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    