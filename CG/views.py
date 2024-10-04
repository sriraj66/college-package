from django.shortcuts import render,redirect
from django.http import JsonResponse
from utils.models import Students
from CG.models import *
from CG.constants import *
from CG.cg import Career_Tool
from django.contrib.auth.decorators import login_required
from authentication.views import load_config

@login_required
def cg(request):
    context = load_config(request)
    if context['profile'].check_credit() is False:
        
        return redirect("err","No Credit Left!!")
    try:
        student = Students.objects.get(user=request.user)
    except Exception as e:
        return render(request,"error.html",{"error": "Login as Student"})
    
    context['ct'] = CareerTool.objects.filter(user=student.user)
    
    return render(request,'CG/cg.html',context)

def linked_in(request):
    context = load_config(request)
    return render(request,'CG/stage.html',context)

def generate_sa(request):
    context = {
        "output":""
    }
    print("SA")
    if request.POST:
        strength = request.POST.get("strength")
        technical_skill = request.POST.get("technical_skill")
        future_roll = request.POST.get("future_roll")
        config = load_config(request)
        
        ct = Career_Tool(request,api_key=config['profile'].college.api_key)
        responce = ct.self_assement(strength, technical_skill, future_roll)
        # context['profile'].reduce_credits(2)
        
        
        context['output'] = responce
    return JsonResponse(context)
    
    
@login_required
def generate_final_map(request):
    context = {
        "output":"",
        # "linkedin":"",
    }
    
    if request.POST:
        ipic = request.POST.get("ipic")
        role = request.POST.get("role")
        workspace = request.POST.get("currently")
        loc = request.POST.get("location")
        ps = request.POST.get("ps")
        gc = request.POST.get("gc")
        config = load_config(request)
        
        ct = Career_Tool(request,api_key=config['profile'].college.api_key)
        responce = ct.generate_final(ipic,role,workspace,loc,ps,gc)
        linkedin = ct.generate_linked_in(config['profile'].name,responce)
        context['output'] = responce
        
        
        
        # context['linkedin'] = linkedin
        
        
        obj = CareerTool(
            user = request.user,
            messages = request.session["ct_message"],
            output = responce,
            goal = ipic,
            linked_in = linkedin,
        )
        obj.save()
        
        config['profile'].CT_usage.add(obj)
        config['profile'].save()
        config['profile'].reduce_credits(4)
        
        
    return JsonResponse(context)
    