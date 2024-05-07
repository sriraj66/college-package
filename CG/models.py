from django.db import models
from utils.models import User
from django.urls import reverse 

class CareerTool(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CT_user')
    goal = models.CharField(max_length=255,blank=True)
    messages = models.TextField(default="")
    linked_in = models.TextField(default="")
    output = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)    
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self) -> str:
        return f"{self.id} - {self.goal}"
    
    
    def get_absolute_url(self):
        return reverse('generate_linkedin_prompt', kwargs={'id': self.id})
    
    
    
    
