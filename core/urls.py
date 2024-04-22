
from django.urls import path
from .views import *

urlpatterns = [
    path("college",college_form,name='college_form'),
    path("getcode/<str:uuid>", source_code, name="source_code"),
    path('api/get_responce',get_chat_responce,name='api_get_responce'),
    path("chatlist",chatbotlist,name='chatbotlist'),    
    path("",index,name='index'),
]
