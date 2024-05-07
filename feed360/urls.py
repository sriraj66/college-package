from django.urls import path
from .views import *

urlpatterns = [
    path("",feed360,name='feed360'),
    path("create/<int:id>",create_form,name='create_form'),
    path("create/question/<int:id>",create_question,name='create_question'),
    path("form/<int:id>/view",view_form,name='view_form'),
    path("form/<int:id>/delete",delete_form,name='delete_form'),
    path("question/<int:id>/edit",edit_question,name='edit_question'),
    path("question/<int:id>/delete",delete_question,name='delete_question'),
    
    path("analysis/<int:id>",sentimental_analysis,name='sentimental_analysis'),
    path("analysis/exel",analysis_with_exel,name='analysis_with_exel')
]