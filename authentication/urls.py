from django.urls import path
from .views import *
urlpatterns = [
    # path("login",login_view,name='login'),
    path("logout/get",logout_get,name='logout_get'),
    path("err/?=<str:err>hluiUYDCD23tyvf",render_error,name='err'),
]