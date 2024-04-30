from django.urls import path
from CG.views import *

urlpatterns = [
    path("",cg,name='cg'),

    path("map/optimizer",linked_in,name='linked_in'),
    path("map/selfasscement",generate_sa,name='generate_sa'),
    path("map/final",generate_final_map,name='generate_final_map'),
]