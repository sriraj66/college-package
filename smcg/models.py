from django.db import models

# Create your models here.
class CONTENTS(models.Model):

    platform = models.CharField(max_length=50)
    post_type = models.CharField(max_length=50)
    goal = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    desc = models.TextField()

    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.platform