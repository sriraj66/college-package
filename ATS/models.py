from django.db import models
from core.models import *
class ATS(models.Model):
    college = models.ForeignKey(College,on_delete=models.CASCADE)

    jd = models.TextField()
    file = models.FileField()

    responce = models.TextField()

    created = models.DateTimeField(auto_now_add=True)



