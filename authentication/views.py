from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.messages import success,error,warning
from django.contrib.auth.decorators import login_required 
from utils.models import Students,Staffs
from django.conf import settings


def load_config(request):
    try:
        if request.user.is_staff or request.user.is_superuser:
            profile = Staffs.objects.get(user=request.user)
        else:
            profile = Students.objects.get(user=request.user)
        
        context = {
            'profile': profile,
            'complete_triger': True,
            "version": settings.VERSION or "beta"
        }
        
        return context
    except Exception as e:
        print(e)
        return {
            "version": settings.VERSION or "beta"
        }


def render_error(request,err):
    config = load_config(request)
    config['error'] = err
    return render(request,'error.html',config)

def logout_get(request):
    return render(request, 'registration/logged_out.html')