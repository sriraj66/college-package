from django.db import models
from django.contrib.auth.models import User
import uuid 

class College(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    
    name = models.CharField(max_length=255,)
    desc = models.TextField(verbose_name="Description")
    
    logo = models.URLField(verbose_name="Logo URL",default="https://images.vexels.com/media/users/3/155806/isolated/preview/b29d14472d5272374a754e05554f03ae-hexagon-icon.png")

    api_key = models.CharField(max_length=255,blank=True)

    root_url = models.URLField(verbose_name="Source URL")
    aditional_urls = models.TextField(blank = True,)
    state = models.BooleanField(default=False)
    
    running = models.BooleanField(default=False)
    
    hints = models.TextField(verbose_name="Hints")
    
    
    messages = models.ManyToManyField('Messages', blank=True) 
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created', '-updated']
    def count_messages(self):
        return len(self.messages)


class Messages(models.Model):
    to = models.ForeignKey(College,on_delete=models.CASCADE, related_name='messages_of_college')
    
    request = models.CharField(max_length=255)
    responce = models.CharField(max_length=255)
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return f"{self.to.name} - {str(self.request)}"
    
    class Meta:
        ordering = ['-created', '-updated']
    