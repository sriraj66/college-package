from django.db import models
from django.contrib.auth.models import User
from CP.models import CoursePlan
from CG.models import CareerTool
from ATS.models import ATS
from smcg.models import CONTENTS
import uuid
from utils.signals import *


GENDER = (
    ('Male','Male'),
    ('Female','Female'),
    ("None","None"),
)

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

    student_credit = models.IntegerField(default=0,verbose_name='credit per Student')
    staff_credit = models.IntegerField(default=100,verbose_name='credit per Staff')

    staffs = models.ManyToManyField('Staffs',verbose_name='Staffs',blank=True)
    students = models.ManyToManyField('Students',verbose_name='Students',blank=True)

    banner = models.ImageField(upload_to="SMCG/Banners",default="defaults/default.png")

    logs = models.ManyToManyField('Logs',verbose_name="logs",blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.short_name} - {str(self.uid)}"

    def CPS(self):
        student_count = self.students.count()
        if student_count > 0:
            return int(self.a_credit / (student_count))
        else:
            return 0

        
    

class Students(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="student")
    
    profile = models.ImageField(upload_to="Users/profiles/",default="defaults/profile.png")
    
    name = models.CharField(max_length=255,verbose_name='Name',blank=True)
    roll = models.CharField(max_length=15,verbose_name='Roll Number',blank=True)
    degree = models.CharField(max_length=100,verbose_name='Degree',blank=True)
    branch = models.CharField(max_length=100,verbose_name='Department',blank=True)
    year = models.IntegerField(default=1,verbose_name="Year")
    
    phone = models.CharField(max_length=12,verbose_name='Phone Number',blank=True)
    gender = models.CharField(max_length=15,choices=GENDER,default="None")
    
    college = models.ForeignKey(CollegeAdmin,null=True,on_delete=models.CASCADE,related_name='student_college')
    
    credit_used = models.IntegerField(default=0,verbose_name="Usage")
    
    is_completed = models.BooleanField(default=False,verbose_name="Profile Completed?")
    
    ATS_usage = models.ManyToManyField(ATS, blank=True,verbose_name="ATS History")
    SMCG_usage = models.ManyToManyField(CONTENTS, blank=True,verbose_name="SMCG History")
    CT_usage = models.ManyToManyField(CareerTool, blank=True,verbose_name="CT History")
    linkedin_usage = models.PositiveIntegerField(default=0,verbose_name="Linked In Usage")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} "
    
    def balance_credit(self):
        try:
            return self.college.student_credit - self.credit_used
        except Exception as e:
            return self.college.student_credit
        
    def calculate_credit(self):
        return self.ATS_usage.count() + self.CT_usage.count() + self.SMCG_usage.count() + self.linkedin_usage

    def check_credit(self):
        if self.calculate_credit() <= self.college.student_credit and self.balance_credit() > 0:
            return True
        
        return False
    
    def reduce_credits(self,amt=2   ,service=None):
        self.credit_used+=amt
        if service == 'li':
            self.linkedin_usage+=amt
        self.save()
    

class Staffs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Staff")
    profile = models.ImageField(upload_to="Users/profiles/",default="defaults/profile.png")
    
    name = models.CharField(max_length=255,verbose_name='Name',blank=True)
    roll = models.CharField(max_length=15,verbose_name='Staff ID',blank=True)
    degree = models.CharField(max_length=100,verbose_name='Degree',blank=True)
    branch = models.CharField(max_length=100,verbose_name='Department',blank=True)
    phone = models.CharField(max_length=12,verbose_name='Phone Number',blank=True)
    gender = models.CharField(max_length=15,choices=GENDER,default="None")
    college = models.ForeignKey(CollegeAdmin,on_delete=models.CASCADE,related_name='staff_college',null=True)
    
    
    is_smcg = models.BooleanField(default=False,verbose_name="Admin SocialMedia Post")
    is_admin = models.BooleanField(default=False,verbose_name="Admin")
    is_completed = models.BooleanField(default=False,verbose_name="Profile Completed?")

    ATS_usage = models.ManyToManyField(ATS, blank=True,verbose_name="ATS History")
    CP_usage = models.ManyToManyField(CoursePlan, blank=True,verbose_name="CP History")
    SMCG_usage = models.ManyToManyField(CONTENTS, blank=True,verbose_name="SMCG History")

    credit_used = models.IntegerField(default=0,verbose_name="Usage")


    def __str__(self):
        if self.user.is_superuser:
            return f"SUPER : {self.user.username}"
        else : 
            return f"{self.user.username} - {self.college.short_name}"
            
    def balance_credit(self):
        try:
            return self.college.staff_credit - self.credit_used
        except Exception as e:
            return self.college.staff_credit
        
    def calculate_credit(self):
        return self.ATS_usage.count() + self.CP_usage.count() + self.SMCG_usage.count()
    
    def reduce_credits(self,amt=2):
        self.credit_used+=amt
        self.save()
    
    def check_credit(self):
        if self.calculate_credit() <= self.college.student_credit and self.balance_credit() > 0:
            return True
        
        return False

    
class Logs(models.Model):
    
    log = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    
    


from django.db.models.signals import *


def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        print("Creating user profile for ",instance.username,instance.is_staff)
        if instance.is_staff or instance.is_superuser:
            Staffs.objects.create(user=instance,name=instance.first_name+" "+instance.last_name)
        else:
            Students.objects.create(user=instance,name=instance.first_name+" "+instance.last_name)
        
        print(f"Profile created for {instance.username}")

  

m2m_changed.connect(update_student_credit, sender=Students.SMCG_usage.through)
m2m_changed.connect(update_student_credit, sender=Students.ATS_usage.through)
m2m_changed.connect(update_student_credit, sender=Students.CT_usage.through)
pre_save.connect(update_college_credit, sender=CollegeAdmin)
post_save.connect(create_user_profile, sender=User)




