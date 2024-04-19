from django.db import models
from utils.models import *

class ATS(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ats_user')

    jd = models.TextField()
    file = models.FileField(upload_to="ATS/resumes")

    responce = models.TextField()
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']

    def get_display_name(self):
        return f"ATS{self.id}"


