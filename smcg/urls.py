from django.urls import path

from .views import *

urlpatterns = [
    path("smcg",generate_social_media_content,name='generate_social_media_content'),
    path("about_post",about_post,name='about_post')
]