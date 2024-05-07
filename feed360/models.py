from django.db import models
from utils.models import Staffs,Students
from django.urls import reverse
import os

FIELD_TYPE = (
    ('Text','Text'),
    ("Rating",'Rating'),
    ('Boolean','Boolean')
)

class Form(models.Model):
    
    staff = models.ForeignKey(Staffs,on_delete=models.CASCADE)

    name = models.CharField(max_length=255,default="Untitled")
    qr = models.ImageField(upload_to="feed360/QR",blank=True)
    questions = models.ManyToManyField('Questions',verbose_name="Questions",blank=True)
    responses  = models.ManyToManyField('Response',verbose_name="Responses",blank=True) 
    
    recivers = models.ManyToManyField(Students,verbose_name="Recivers",blank=True)
    
    analysis = models.ManyToManyField('Analysis',verbose_name="Analysis")
    
    created = models.DateTimeField(auto_now_add=True)

    def get_responce_count(self):
        try:
            return int(self.responses.count()/self.questions.count())
        except:
            return 0
    def __str__(self) -> str:
        return f"id : {self.id} By : {self.staff.name}"

    def get_absolute_url(self):
        return reverse('view_form', kwargs={'id': self.id})
    

class Analysis(models.Model):
    form_id = models.ForeignKey(Form,on_delete=models.CASCADE,related_name="form_id_analysis")
    
    report = models.TextField()
    
    class Meta:
        ordering = ['-id']
    
class Questions(models.Model):
    staff = models.ForeignKey(Staffs,on_delete=models.CASCADE)
    form_id = models.ForeignKey(Form,related_name="root_form_id_question",verbose_name="Form",on_delete=models.CASCADE,blank=True,null=True)
    question = models.CharField(max_length=255,verbose_name="Question")
    field_type = models.CharField(max_length=50,choices=FIELD_TYPE,default=0,verbose_name="Field Type")
    
    def __str__(self) -> str:
        return f"{self.question}"
    
class Response(models.Model):
    
    student = models.ForeignKey(Students,verbose_name="Student",on_delete=models.CASCADE)
    question = models.ForeignKey(Questions,verbose_name="Question",on_delete=models.CASCADE)
    response = models.CharField(max_length=255,blank=True)
    
    form_id = models.ForeignKey(Form,related_name="root_form_id",verbose_name="Form",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.response
    
class Analysis_with_exel(models.Model):
    staff = models.ForeignKey(Staffs,related_name="Exel_form_staffs",on_delete=models.CASCADE)
    file = models.FileField(upload_to='feed360/from_exel',blank=True)
    report = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
     
    @property
    def file_name(self):
        
        return os.path.basename(self.file.name)
