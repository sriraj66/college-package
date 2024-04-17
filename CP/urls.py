from django.urls import path
from CP.views import *

urlpatterns = [
    path("",cp,name='cp'),
    path("course_map",course_map,name='course_map'),
    path("course_map/his",full_history,name='cp_history'),
    path("course_map/<int:id>",view_record,name='cp_record'),

]
