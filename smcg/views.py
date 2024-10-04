from django.shortcuts import render,redirect
from smcg.constants import *
from django.http import JsonResponse
from smcg.smcg import *
from smcg.generate_image import GenerateImage
from smcg.models import *
from utils.models import Staffs,Students
from django.contrib.auth.decorators import login_required
from authentication.views import load_config

@login_required
def generate_social_media_content(request):
    user = User.objects.get(id=request.user.id)
    new_typ = TYPE.copy()
    new_goal = GOAL.copy()
    try:
        
        if user.is_staff or user.is_superuser:
            profile = Staffs.objects.get(user=user)
            if profile.is_smcg is False:
                new_typ.remove("Image")
        else:
            profile = Students.objects.get(user=user)
            new_typ.remove("Image")
            new_typ.remove("Story")
            new_typ.remove("Infographic")
            new_typ.remove("Testimonial")
            new_goal.remove("Convince")
            new_goal.remove("Important_days")
            new_goal.remove("Holidays")
    
    except Exception as e:
        return redirect("err",e)
        

    context = load_config(request)
    if context['profile'].check_credit() is False:
        
        return redirect("err","No Credit Left!!")
    
    context['platform']=PLATFORM
    context['goals']= new_goal
    context['types']= new_typ
    context['idea']= IDEA
    context['uids'] =ChatBot.objects.filter(college= profile.college) or ["None"]
    
    del new_typ
    context['profile'].reduce_credits(1)

    return render(request,"smcg/smcg.html",context)


@login_required
def about_post(request):
    return JsonResponse(IDEA)


def generate_image(id,key,responce,desc,header):
    
    obj = GenerateImage(id=id,key=key,content=responce,extra=desc)
    gen_img =  obj.combine_images(header)
    print("Image Generated...")
    
    return gen_img
    

@login_required
def gen_smcg(request):
    context = {
        "output":"No Output",
        "image":False,
    }
    if request.POST:
        try:
            user = User.objects.get(id=request.user.id)
            allow_image = False
            if user.is_staff or user.is_superuser:
                profile = Staffs.objects.get(user=user)
                allow_image = profile.is_smcg or False
            else:
                profile = Students.objects.get(user=user)
                allow_image = False
                
            plt = request.POST.get("platform")
            pt = request.POST.get("post_type")
            goal = request.POST.get("goal")
            topic = request.POST.get("topic")
            des = request.POST.get("des")
            
            uuid = request.POST.get("uuid","None")
            if uuid == "None":
                uuid = None
            is_image = True if pt == 'Image' and allow_image is True  else False
            
            is_past = True if request.POST.get("past",False) == 'true' else False
            clg = profile.college
            
            print("UUID : ",uuid)
            print("Past : ",is_past)
            
            
            print("Generating ..")
            obj = SMCG(key=clg.api_key,uid=uuid,is_past=is_past)
            
            responce = obj.get_content(request,platform=plt,type=pt,goal=goal,topic=topic,desc=des)
            
            context['output'] = responce
            context["image"] = is_image
            con = CONTENTS(user = request.user,
                            platform=plt,
                            post_type=pt,
                            goal=goal,
                            topic=topic,
                            desc=des,
                            responce=context['output'],
                            is_image=is_image)
            con.save()
            profile.reduce_credits(2)
            
            print("Is Image : ",is_image)
            if is_image is True and uuid is not None:
                header = profile.college.banner.url 
                out = generate_image(con.id,clg.api_key,responce,des,header=header)
                print("Out : ",out)
                if out == True:
                    print("Image Saved")
                    profile.reduce_credits(10)
                    
                    context["image"] = CONTENTS.objects.get(id=con.id).output_image.url
                    print(context["image"])
                    print(context)
                else:
                    print("Image Not Saved")
                    context["image"] = False
                    
            profile.SMCG_usage.add(con)
            profile.save()

        except Exception as e:
            context['output'] = e
            context["image"] = False

    return JsonResponse(context)


@login_required
def full_history(request):
    if request.user.is_staff or request.user.is_superuser:
        profile = Staffs.objects.get(user=request.user)
    else:
        profile = Students.objects.get(user=request.user)
        
    context = {
        'profile': profile,
        'records': profile.SMCG_usage.all(),
    }
    return render(request,'smcg/history.html',context)