from django.urls import path
from CP.views import *

urlpatterns = [
    path("",cp,name='cp'),
    path("course_map",course_map,name='course_map')
]
