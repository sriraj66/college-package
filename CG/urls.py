from django.urls import path
from CG.views import *

urlpatterns = [
    path("",cg,name='cg'),
    path("map/",road_map,name='road_map'),
    path("map/his",full_history,name='cg_history'),
    path("map/<int:id>",view_record,name='cg_record'),
]