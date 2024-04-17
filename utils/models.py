from django.db import models
from django.contrib.auth.models import User
from CP.models import CoursePlan
from CG.models import CG
from ATS.models import ATS
from smcg.models import CONTENTS
import uuid


class CollegeAdmin(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="admin")
    name = models.CharField(max_length=255,verbose_name='College Name')
    short_name = models.CharField(max_length=100,verbose_name='Short Name')
    web_url = models.URLField(verbose_name='Website')
    icon = models.URLField(verbose_name='Fav Icon',default="https://images.vexels.com/media/users/3/155806/isolated/preview/b29d14472d5272374a754e05554f03ae-hexagon-icon.png")
    
    api_key = models.CharField(max_length=255,verbose_name='API Key')


    a_credit = models.IntegerField(default=0,verbose_name='Credit')
    b_credit = models.IntegerField(default=0,verbose_name='Balance Credit')
    c_credit = models.IntegerField(default=0,verbose_name='Usage')

    staffs = models.ManyToManyField('Staffs',verbose_name='Staffs',blank=True)
    students = models.ManyToManyField('Students',verbose_name='Students',blank=True)

    banner = models.ImageField(upload_to="SMCG/Banners",default="defaults/default.png")

    logs = models.ManyToManyField('Logs',verbose_name="logs",blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.short_name} - {str(self.uid)}"


class Students(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="student")
    
    profile = models.ImageField(upload_to="Users/profiles/",default="defaults/profile.png")
    
    name = models.CharField(max_length=255,verbose_name='Name',blank=True)
    roll = models.CharField(max_length=15,verbose_name='Roll Number',blank=True)
    degree = models.CharField(max_length=100,verbose_name='Degree',blank=True)
    branch = models.CharField(max_length=100,verbose_name='Department',blank=True)
    year = models.IntegerField(default=1,verbose_name="Year")
    
    phone = models.CharField(max_length=12,verbose_name='Phone Number',blank=True)
    gender = models.CharField(max_length=10,default="None")
    
    college = models.ForeignKey(CollegeAdmin,on_delete=models.CASCADE,related_name='student_college')
    
    ATS_usage = models.ManyToManyField(ATS, blank=True,verbose_name="ATS History")
    CG_usage = models.ManyToManyField(CG, blank=True,verbose_name="CG History")
    SMCG_usage = models.ManyToManyField(CONTENTS, blank=True,verbose_name="SMCG History")
    
    created = models.DateTimeField(auto_now_add=True)
    
    
    


class Staffs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Staff")
    profile = models.ImageField(upload_to="Users/profiles/",default="defaults/profile.png")
    
    name = models.CharField(max_length=255,verbose_name='Name',blank=True)
    roll = models.CharField(max_length=15,verbose_name='Staff ID',blank=True)
    degree = models.CharField(max_length=100,verbose_name='Degree',blank=True)
    branch = models.CharField(max_length=100,verbose_name='Department',blank=True)
    phone = models.CharField(max_length=12,verbose_name='Phone Number',blank=True)
    gender = models.CharField(max_length=10,default="None")
    college = models.ForeignKey(CollegeAdmin,on_delete=models.CASCADE,related_name='staff_college')
    
    
    is_smcg = models.BooleanField(default=False,verbose_name="Admin SocialMedia Post")

    ATS_usage = models.ManyToManyField(ATS, blank=True,verbose_name="ATS History")
    CP_usage = models.ManyToManyField(CoursePlan, blank=True,verbose_name="CP History")
    SMCG_usage = models.ManyToManyField(CONTENTS, blank=True,verbose_name="SMCG History")


class Logs(models.Model):
    
    log = models.TextField()
    created = models.DateTimeField(auto_now_add=True)