from django.urls import path

from smcg.views import *

urlpatterns = [
    path("smcg",generate_social_media_content,name='generate_social_media_content'),
    path("about_post",about_post,name='about_post'),
    path("gen/",gen_smcg,name='gen_smcg'),
    path("gen/his",full_history,name='smcg_history'),
]