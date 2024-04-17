from django.db import models
from utils.models import User

class CONTENTS(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="smcg_user")
    
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