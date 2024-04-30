from django.db import models
from utils.models import User

class CareerTool(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CT_user')

    messages = models.TextField(default="")
    linked_in = models.TextField(default="")
    output = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)    
    
    class Meta:
        ordering = ['-created']
    
    
