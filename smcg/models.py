from django.db import models
from core.models import College

class CONTENTS(models.Model):
    clg = models.ForeignKey(College,on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    post_type = models.CharField(max_length=50)
    goal = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    desc = models.TextField()

    responce = models.TextField(blank=True)
    
    is_image = models.BooleanField(default=False)

    # default_image = models.ImageField(upload_to="SMCG/Header",default="defaults/krct.jpg",blank=True)
    
    output_image = models.ImageField(upload_to="SMCG/output",blank=True)


    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.platform