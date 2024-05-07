from django.urls import path
from .views import *

urlpatterns = [
    path("",linkedin,name="linkedin"),
    path("gen/<int:id>",generate_linkedin_prompt,name="generate_linkedin_prompt"),
]