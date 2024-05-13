from django.urls import path
from .views import *

urlpatterns = [
    path("",rb,name="rb"),
    path("create/<int:id>",create_resume,name="create_resume"),
    path("delete/<int:id>",delete_resume,name="delete_resume"),
    path("templates<str:uid>/view",resume_templates,name="resume_templates"),
]

hx_urls = [
    path("create/skill@for<int:id>/",create_skill,name='create_skill'),
    path('delete@skill/<int:rid>/@<int:sid>',delete_skill,name='delete_skill'),
    
    path("create/edu@for<int:id>/",create_edu,name='create_edu'),
    path('delete@edu/<int:rid>/@<int:sid>',delete_edu,name='delete_edu'),
    
    path("create/ach@for<int:id>/",create_ach,name='create_ach'),
    path('delete@ach/<int:rid>/@<int:sid>',delete_ach,name='delete_ach'),
    
    
    path("create/pro@for<int:id>/",create_pro,name='create_pro'),
    path('delete@pro/<int:rid>/@<int:sid>',delete_pro,name='delete_pro'),
    
    path("create/soc@for<int:id>/",create_soc,name='create_soc'),
    path('delete@soc/<int:rid>/@<int:sid>',delete_soc,name='delete_soc'),
    
    path("create/lang@for<int:id>/",create_lang,name='create_lang'),
    path('delete@lang/<int:rid>/@<int:sid>',delete_lang,name='delete_lang'),
    
]

urlpatterns += hx_urls