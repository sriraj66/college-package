from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from authentication.views import load_config
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from .forms import ResumeForm,SocialForm,LangForm


@login_required
def rb(request):
    context = load_config(request)
    
    context['rb'] = Resume.objects.filter(user=request.user)
    context['temps'] = [[1,"Simple Resume Template"],[2,'Minimal Resume Template']]
    
    if request.POST:
        
        res = Resume(
            user = request.user,
            role = "",
            bio = "Your Bio..!"
        )
        res.save()
        success(request,"Complete the Resume details")

        return redirect('create_resume',res.id)
        
    return render(request,"resumebuilder/rb.html",context)

def delete_resume(request,id):
    
    if request.method == "POST":
        res = Resume.objects.get(id=id)
        res.delete()
        success(request,"Sucessfully deleted")
    else:
        success(request,"Invalid Request",extra_tags='danger')    
            
    return redirect('rb')

def resume_templates(request,uid):
    context = load_config(request)
    context['rb'] = Resume.objects.get(uid=uid)
    
    if not context['rb'].user.is_staff:
        context['pro'] = Students.objects.get(user = context['rb'].user)
        
    if request.method == "POST":
        tid = request.POST.get("tid",1)
        context['rb'].template_id = int(tid)
        context['rb'].save()
    
    if request.method in ['POST','GET']:    
        template_name = f"resume{context['rb'].template_id}.html"    
        return render(request,f"resumebuilder/templates/{template_name}",context)
    
    
    success(request,"Invalid Request",extra_tags="danger")
    return redirect("rb")

@login_required
def create_resume(request,id):
    context = load_config(request)
    
    instance = Resume.objects.get(id=id)
    context['rb'] = instance
    
    if request.method == 'POST':

        form = ResumeForm(request.POST,request.FILES, instance=instance,user = request.user)
        if form.is_valid():
            form.save()
            context['form'] = form           
            return render(request,"resumebuilder/partial/edit.html",context)

    else:
        form = ResumeForm(instance=instance,user = request.user)
        soc_form = SocialForm(instance=instance)
        lang_form = LangForm(instance=instance)
    
    context['form'] = form
    context['social_form'] = soc_form
    context['lang_form'] = lang_form
    return render(request,'resumebuilder/create.html',context)
@login_required
def create_skill(request,id):
    context = load_config(request)
    instance =  Resume.objects.get(id=id)
    context['rb'] = instance
    if request.POST:
        form = ResumeForm(instance=instance,user = request.user)
        skill = request.POST.get("skill","")
        
        if len(skill) > 0:    
            obj = Skill(
                res = instance,
                skill = skill
            )
            obj.save()
            context['form'] = form
        return render(request,'resumebuilder/partial/skills.html',context)
        
    return render(request,'resumebuilder/partial/skill_form.html',context)
@login_required
def delete_skill(request,rid,sid):
    context = load_config(request)
    instance =  Resume.objects.get(id=rid)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Skill.objects.get(id=sid)
        obj.delete()
        
    return render(request,'resumebuilder/partial/skills.html',context)

@login_required
def create_edu(request,id):
    context = load_config(request)
    
    instance = Resume.objects.get(id=id)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Education(
            res=instance,
            school = request.POST.get("school").title(),
            course = request.POST.get("course"),
            per = request.POST.get("per"),
            place = request.POST.get("place").title(),
            yog = request.POST.get("yog"),
            is_completed = True if request.POST.get("is_completed") == 'on' else False
        )
        obj.save()
        
    return render(request,'resumebuilder/partial/edu.html',context)

@login_required
def delete_edu(request,rid,sid):
    context = load_config(request)
    instance =  Resume.objects.get(id=rid)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Education.objects.get(id=sid)
        obj.delete()
        
    return render(request,'resumebuilder/partial/edu.html',context)

@login_required
def create_ach(request,id):
    context = load_config(request)
    
    instance = Resume.objects.get(id=id)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Achivement(
            res=instance,
            title = request.POST.get("title").title(),
            desc = request.POST.get("desc").title(),
            place = request.POST.get("place").title(),
            date = request.POST.get("yog").title(),
        )
        obj.save()
        
    return render(request,'resumebuilder/partial/ach.html',context)

@login_required
def delete_ach(request,rid,sid):
    context = load_config(request)
    instance =  Resume.objects.get(id=rid)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Achivement.objects.get(id=sid)
        obj.delete()
        
    return render(request,'resumebuilder/partial/ach.html',context)


@login_required
def create_pro(request,id):
    context = load_config(request)
    
    instance = Resume.objects.get(id=id)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Projects(
            res=instance,
            title = request.POST.get("title").title(),
            description = request.POST.get("desc").title(),
            url = request.POST.get("url").title(),
        )
        obj.save()
        
    return render(request,'resumebuilder/partial/pro.html',context)

@login_required
def delete_pro(request,rid,sid):
    context = load_config(request)
    instance =  Resume.objects.get(id=rid)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Projects.objects.get(id=sid)
        obj.delete()
        
    return render(request,'resumebuilder/partial/pro.html',context)


@login_required
def create_soc(request,id):
    context = load_config(request)
    
    instance = Resume.objects.get(id=id)
    context['rb'] = instance
    
    if request.method == 'POST':
        form = SocialForm(request.POST,resume=instance)
        if form.is_valid():
            form.save()
    else:
        form = SocialForm(resume=instance)
        
    context['social_form'] = form
    return render(request,'resumebuilder/partial/soc.html',context)

@login_required
def delete_soc(request,rid,sid):
    context = load_config(request)
    instance =  Resume.objects.get(id=rid)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Socials.objects.get(id=sid)
        obj.delete()

    return render(request,'resumebuilder/partial/soc.html',context)


@login_required
def create_lang(request,id):
    context = load_config(request)
    
    instance = Resume.objects.get(id=id)
    context['rb'] = instance
    
    if request.method == 'POST':
        form = LangForm(request.POST,resume=instance)
        if form.is_valid():
            form.save()
    else:
        form = LangForm(resume=instance)
        
    context['lang_form'] = form
    return render(request,'resumebuilder/partial/lang.html',context)

@login_required
def delete_lang(request,rid,sid):
    context = load_config(request)
    instance =  Resume.objects.get(id=rid)
    context['rb'] = instance
    
    if request.method == 'POST':
        obj = Languages.objects.get(id=sid)
        obj.delete()

    return render(request,'resumebuilder/partial/lang.html',context)
