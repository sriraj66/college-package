from django.db import models
from utils.models import User

class CG(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CG_user')
        
    sd = models.TextField()

    jd = models.CharField(max_length=255)
    loc = models.CharField(max_length=50,default="India")
    sal = models.CharField(max_length=10)
    skills = models.TextField()
    duration = models.CharField(max_length=100,default="4")
    
    
    output = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    
    