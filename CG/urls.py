from django.urls import path
from CG.views import *

urlpatterns = [
    path("",cg,name='cg'),
    path("map/",road_map,name='road_map')
]