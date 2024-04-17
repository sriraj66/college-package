from django.urls import path
from .views import *
urlpatterns = [
    path("",ats,name='ats'),
    path("ats/ev",ats_ev,name="ats_ev"),
    path("ats/his",full_history,name="ats_history"),
    path("ats/<int:id>",view_record,name="ats_record")

]