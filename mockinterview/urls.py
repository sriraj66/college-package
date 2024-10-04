from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name='mi'),    
    path("proc/<int:id>",process,name='process'),
    path("proc-check/<int:id>",interview_check,name='interview_check'),
    path("proc/res<int:id>",process_result,name='process_result'),
]
