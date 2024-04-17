from django.shortcuts import render
from django.http import JsonResponse
from CG.models import *
import json
from CG.constants import *
from CG.cg import MAP
from utils.models import Students,Staffs
from django.contrib.auth.decorators import login_required
from authentication.views import load_config

@login_required
def cg(request):
    context = load_config(request)
    
    try:
        student = Students.objects.get(user=request.user)
    except Exception as e:
        return render(request,"error.html",{"error": "Login as Student"})
    
    context["degree"]=[student.degree]
    context["branch"]=[student.branch]
    context["year"] =[student.year]
    
    
    return render(request,'CG/cg.html',context)


def road_map(request):
    context = {
        "output":""
    }
    
    if request.POST and request.user.is_authenticated:
        student = Students.objects.get(user=request.user)
        
        sd = request.POST.get("sd")
        sj = request.POST.get("dj"," ")
        dur = request.POST.get("dur")
        loc = request.POST.get("loc")
        sal = request.POST.get("sal")
        skill = request.POST.get("skill")

        obj = CG(
            user=request.user,
            sd=sd,jd=sj,loc=loc,sal=sal,skills=skill,
            duration=dur
        )
        
        app = MAP(student.college.api_key)
        n = app.set_prompt(name=student.name, year=student.year,deg=student.degree,branch=student.branch,sd=sd,dur=dur,jd=sj,loc=loc,se=sal,skills=skill)
        if n is True:
            responce = app.generate()
            print(responce)
            try:    
                obj.output = responce
                responce = json.loads(responce)
                print(responce)
                context = responce
            except Exception as e:
                print(e)
                
        obj.save()
        
        student.CG_usage.add(obj)
        student.save()
        
        
    return JsonResponse(context)


@login_required
def full_history(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'error.html', {'error':'Access Denied'})
    else:
        profile = Students.objects.get(user=request.user)
    context = {
        'profile': profile,
        'records': profile.CG_usage.all().order_by("-created"),
    }
    return render(request,'CG/history.html',context)

@login_required
def view_record(request,id):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'error.html', {'error':'Access Denied'})
    else:
        profile = Students.objects.get(user=request.user)
    context = {
        'profile': profile,
        'record': profile.CG_usage.get(id=id),
    }
    
    return render(request,'CG/view.html',context)