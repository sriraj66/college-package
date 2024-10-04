from django.db import models
from core.models import User



class InterviewResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.TextField(verbose_name="Message", blank=True)
    result = models.TextField("Result", blank=True)
    
    is_ended = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    

class CreateInterview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='interviewAdmin')
    role = models.CharField(max_length=255, verbose_name="Job Role")
    description = models.TextField(verbose_name="Description")
    
    attendee = models.ManyToManyField(User,blank=True,related_name="Iattendee")
    attendence = models.ManyToManyField(InterviewResult,blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    def user_interview(self,user):
        return self.attendee.filter(id=user.id).exists()
    
    
    def __str__(self) -> str:
        return self.role
