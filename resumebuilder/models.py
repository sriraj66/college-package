from django.db import models
from utils.models import User,Students
import uuid

class Achivement(models.Model):
    res = models.ForeignKey('Resume', on_delete=models.CASCADE)
    title = models.CharField(max_length=255,verbose_name="Title")
    place = models.CharField(max_length=255,verbose_name="Place")
    date = models.CharField(max_length=255,verbose_name="Date")
    desc = models.CharField(max_length=255,default="",verbose_name="Description")
    def __str__(self) -> str:
        return f"{self.org} - {self.place}"
    
    class Meta:
        ordering = ['-id']


class Education(models.Model):
    res = models.ForeignKey('Resume', on_delete=models.CASCADE)
    
    school = models.CharField(max_length=255,verbose_name="School / College")
    course = models.CharField(max_length=255,verbose_name="Course")
    per = models.CharField(max_length=255,verbose_name="Percentage")
    
    place = models.CharField(max_length=255,verbose_name="Place")
    yog = models.CharField(max_length=255,verbose_name="Year of Completed")
    is_completed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.school} - {self.place}"
    
    class Meta:
        ordering = ['-id']
        
class Projects(models.Model):
    res = models.ForeignKey('Resume', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255,verbose_name="Project Title")
    description = models.TextField(verbose_name="Description")
    url = models.URLField(verbose_name="Attachment",blank=True)
    
    def __str__(self) -> str:
        return f"{self.title}"
    class Meta:
        ordering = ['-id']

class Skill(models.Model):
    res = models.ForeignKey('Resume', on_delete=models.CASCADE)
    
    skill = models.CharField(max_length=150,verbose_name="Skill Name")
    
    def __str__(self) -> str:
        return f"{self.skill}"
    class Meta:
        ordering = ['-id']

class Socials(models.Model):
    PLATFORMS = (
        ("fab fa-linkedin-in","Linkedin"),
        ("fab fa-github","Github"),
        ("fab fa-facebook-f","Facebook"),
        ("fab fa-instagram","Instagram"),
        ("fab fa-twitter","X"),
        ("fas fa-globe","Others")
        )
    res = models.ForeignKey('Resume',on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255,choices=PLATFORMS,default=0,verbose_name="Social Platform")
    url = models.URLField(verbose_name="Profile URL")

    def __str__(self) -> str:
        return f"{self.name}"

class Languages(models.Model):
    LANGUAGE_FLUENCY_TYPES = (
        ("Native", "Native"),
        ("Professional", "Professional"),
        ("Fluent", "Fluent"),
        ("Limited Proficiency", "Limited Proficiency")
    )
    res = models.ForeignKey('Resume', on_delete=models.CASCADE)
    name = models.CharField(max_length=255,verbose_name="Language Name")
    fluency = models.CharField(max_length=255,verbose_name="Fluency",choices=LANGUAGE_FLUENCY_TYPES)

    def __str__(self) -> str:
        return f"{self.name}"

class Resume(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    
    user = models.ForeignKey(User, related_name="resume_user",verbose_name="User",on_delete=models.CASCADE)
    img = models.ImageField(verbose_name="Profile Image",blank=True,upload_to="ResumeBuilder/profiles")
    role = models.CharField(verbose_name="I Am a ",max_length=255)
    bio = models.TextField(verbose_name="Objective or Description")
    
    template_id = models.PositiveSmallIntegerField(default=1)
    
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"{self.id} - {self.user.username}"
    
    def get_skills(self):
        return Skill.objects.filter(res=self.id)
    
    def get_edu(self):
        return Education.objects.filter(res=self.id)
    
    def get_ach(self):
        return Achivement.objects.filter(res=self.id)
    
    
    def get_lang(self):
        return Languages.objects.filter(res=self.id)
    
    def get_pro(self):
        return Projects.objects.filter(res=self.id)
    
    def get_social(self):
        return Socials.objects.filter(res=self.id)
    