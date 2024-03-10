
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path("college",college_form,name='college_form'),
    path("getcode/<str:uuid>", source_code, name="source_code"),
    path('api/get_responce',get_chat_responce,name='api_get_responce'),
]
