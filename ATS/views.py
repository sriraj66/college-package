from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from utils.models import Staffs,Students
from .ats import run
import json
from django.contrib.auth.decorators import login_required
from authentication.views import load_config

@login_required
def ats(request):
    context = load_config(request)
    if context['profile'].check_credit() is False:
        
        return redirect("err","No Credit Left!!")
    return  render(request,"ATS/ATS.html",context)


def ats_ev(request):

    context = {

    }

    
    if request.POST and request.user.is_authenticated:
        
        jd = request.POST.get("jd")

        pdf = request.FILES.get("file")
        user = User.objects.get(id=request.user.id)
        if user.is_staff or user.is_superuser:
            profile = Staffs.objects.get(user=user)    
        else:
            profile = Students.objects.get(user=user)
            
        clg = profile.college
            

        obj = ATS(user=request.user,jd=jd,file=pdf,responce = "0")
        obj.save()
        print(obj.file.url)
        media_path = obj.file.url

        obj.responce = run(clg.api_key,media_path,jd)
        profile.reduce_credits(2)
        context = json.loads(obj.responce)
        obj.rating = context['score']
        obj.save()
        
        profile.ATS_usage.add(obj)
        profile.save()
        
    return JsonResponse(context)

@login_required
def full_history(request):
    if request.user.is_staff or request.user.is_superuser:
        profile = Staffs.objects.get(user=request.user)
    else:
        profile = Students.objects.get(user=request.user)
    context = {
        'profile': profile,
        'records': profile.ATS_usage.all().order_by("-created"),
    }
    return render(request,'ATS/history.html',context)

@login_required
def view_record(request,id):
    context = load_config(request)
    
    context['record'] = ATS.objects.get(id=id)
    
    return render(request,'ATS/view.html',context)