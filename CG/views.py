from django.shortcuts import render
from django.http import JsonResponse
from CG.models import *
import json
from CG.constants import *
from CG.cg import MAP
def cg(request):
    
    context = {
        "degree":degrees,
        "branch":branch,
        "year" :years,
    }
    
    return render(request,'CG/cg.html',context)


def road_map(request):
    context = {
        "output":""
    }
    
    if request.POST:
        
        uid = request.POST.get("uuid")
        name = request.POST.get("name")
        degree = request.POST.get("degree")
        branch = request.POST.get("branch")
        year = request.POST.get("year")
        sd = request.POST.get("sd")
        sj = request.POST.get("dj"," ")
        dur = request.POST.get("dur")
        loc = request.POST.get("loc")
        sal = request.POST.get("sal")
        skill = request.POST.get("skill")

        clg = College.objects.get(uid=uid)
        
        obj = CG(
            clg=clg,
            name=name,
            year = year,deg=degree,branch=branch,
            sd=sd,jd=sj,loc=loc,sal=sal,skills=skill,
            duration=dur
        )
        
        app = MAP(uid)
        n = app.set_prompt(name=name, year=year,deg=degree,branch=branch,sd=sd,dur=dur,jd=sj,loc=loc,se=sal,skills=skill)
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