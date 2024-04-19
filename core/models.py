from django.db import models
from django.contrib.auth.models import User
from utils.models import CollegeAdmin
import uuid

class ChatBot(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    uid = models.UUIDField(default=uuid.uuid4,editable=False)

    college = models.ForeignKey(CollegeAdmin, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255,)
    desc = models.TextField(verbose_name="Description")
    
    logo = models.URLField(verbose_name="Logo URL",default="https://images.vexels.com/media/users/3/155806/isolated/preview/b29d14472d5272374a754e05554f03ae-hexagon-icon.png")

    root_url = models.URLField(verbose_name="Source URL")
    aditional_urls = models.TextField(blank = True,)
    state = models.BooleanField(default=False)
    
    running = models.BooleanField(default=False)
    
    hints = models.TextField(verbose_name="Hints")
    
    messages = models.ManyToManyField('Messages', blank=True) 
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.name}- {str(self.uid)}"

    class Meta:
        ordering = ['-created', '-updated']
    def count_messages(self):
        return len(self.messages)


class Messages(models.Model):
    to = models.ForeignKey(ChatBot,on_delete=models.CASCADE, related_name='messages_of_college')
    
    request = models.TextField()
    responce = models.TextField()
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return f"{self.to.name} - {str(self.request)}"
    
    class Meta:
        ordering = ['-created', '-updated']
    