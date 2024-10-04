from django.shortcuts import render,redirect
from .constants import *
from CP.models import *
from utils.models import Staffs
from django.http import JsonResponse
from CP.cp import *
import json
from django.contrib.auth.decorators import login_required
from authentication.views import load_config

@login_required
def cp(request):
    context = load_config(request)
    if context['profile'].check_credit() is False:
            
            return redirect("err","No Credit Left!!")
    if request.user.is_staff or request.user.is_superuser:
        return render(request,"CP/cp.html",context)
    else:
        return redirect("err","Students not authorized")


@login_required
def course_map(request):
    context = {
        "output":""
    }
    
    if request.POST and request.user.is_authenticated:
        staff = Staffs.objects.get(user=request.user)
        sbranch = request.POST.get("sbranch")
        sub = request.POST.get("sub")
        syl = request.POST.get("syllabus"," ")
        dur = request.POST.get("dur")
        tp = request.POST.get("tp")
        
        obj = CoursePlan(
            user = request.user,
            sbranch = sbranch,
            subject = sub,
            syllbus = syl,
            pd = dur,
            tp = tp
        )
        
        app = CMAP(staff.college.api_key)
        n = app.set_prompt(name=staff.name,major=staff.degree,branch=staff.branch,sBranch=sbranch,subject=sub,syllbus=syl,tp=tp,pd=dur)
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
        staff.CP_usage.add(obj)
        staff.save()
        staff.reduce_credits(5)
        
    return JsonResponse(context)


@login_required
def full_history(request):
    if request.user.is_staff or request.user.is_superuser:
        profile = Staffs.objects.get(user=request.user)
    else:
        return render(request,'error.html',{"error":'Access Denied'})
    context = {
        'profile': profile,
        'records': profile.CP_usage.all(),
    }
    return render(request,'CP/history.html',context)



@login_required
def view_record(request,id):
    if request.user.is_staff or request.user.is_superuser:
        profile = Staffs.objects.get(user=request.user)

    else:
        return render(request, 'error.html', {'error':'Access Denied'})
        
    context = {
        'profile': profile,
        'record': profile.CP_usage.get(id=id),
    }
    print(context['record'].output)
    
    return render(request,'CP/view.html',context)