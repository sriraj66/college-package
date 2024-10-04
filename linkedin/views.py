from django.shortcuts import render,redirect
from django.http import JsonResponse
from CG.cg import Career_Tool as cg_tool
from authentication.views import load_config
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def linkedin(request):
    context = load_config(request)
    
    if request.user.is_staff:
        return redirect("err","Access Denied!!")
    
    context['cm'] = CareerTool.objects.filter(user=request.user)
    context['modes'] = ['Connection Request',"Asking for LinkedIn Endorsement","Asking for recommendations on LinkedIn"]
    
    return render(request,"linkedin/linkedin.html",context)

def generate_linkedin_prompt(request,id):
    context = load_config(request)
    
    output = {
        "output":""
    }

    if request.POST:
        
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        mode = request.POST.get("mode")
        
        ct = CareerTool.objects.get(id=id)
        
        cg = cg_tool(request,context['profile'].college.api_key)
        res = cg.write_modes(name,bio,mode,ct.linked_in)
        context['profile'].reduce_credits(1,service='li')
        
        output['output'] = res 
        
    return JsonResponse(output)