from django.urls import path
from .views import *

urlpatterns = [
    path("profile",my_profile,name='my_profile'),
    path("edit/profile",edit_profile,name='edit_profile'),
    
    path("load_student",load_student,name='load_student'),
    path("view/students",my_students,name='my_students'),
]