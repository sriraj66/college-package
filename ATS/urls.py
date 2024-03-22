from django.urls import path
from .views import *
urlpatterns = [
    path("",ats,name='ats'),
    path("ats/ev",ats_ev,name="ats_ev")
]