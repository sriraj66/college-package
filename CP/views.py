from django.shortcuts import render
from .constants import *
from CP.models import *
from django.http import JsonResponse
from CP.cp import *
import json
def cp(request):
    
    return render(request,"CP/cp.html")

def course_map(request):
    context = {
        "output":""
    }
    
    if request.POST:
        
        uid = request.POST.get("uuid")
        name = request.POST.get("name")
        major = request.POST.get("major")
        branch = request.POST.get("branch")
        sbranch = request.POST.get("sbranch")
        sub = request.POST.get("sub")
        syl = request.POST.get("syllabus"," ")
        dur = request.POST.get("dur")
        tp = request.POST.get("tp")
        
        clg = College.objects.get(uid=uid)
        
        obj = CoursePlan(
            clg=clg,
            name=name,
            major = major,
            branch = branch,
            sbranch = sbranch,
            subject = sub,
            syllbus = syl,
            pd = dur,
            tp = tp
        )
        
        app = CMAP(uid)
        n = app.set_prompt(name=name,major=major,branch=branch,sBranch=sbranch,subject=sub,syllbus=syl,tp=tp,pd=dur)
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
        
    return JsonResponse(context)