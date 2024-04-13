from django.shortcuts import render
from smcg.constants import *
from django.http import JsonResponse
from smcg.smcg import *
from smcg.generate_image import GenerateImage
from django.conf import settings
import os
from smcg.models import CONTENTS
def generate_social_media_content(request):
    context = {
        'platform':PLATFORM,
        'goals': GOAL,
        'types': TYPE,
        'idea': IDEA,
    }

    return render(request,"smcg/smcg.html",context)


def about_post(request):
    return JsonResponse(IDEA)

def generate_image(id,uuid,responce,desc,header):
    
    obj = GenerateImage(id=id,uid=uuid,content=responce,extra=desc)
    gen_img =  obj.combine_images(header)
    print("Image Generated...")
    return gen_img
    


def gen_smcg(request):
    context = {
        "output":"No Output",
        "image":False,
    }
    if request.POST:
        try:
            plt = request.POST.get("platform")
            pt = request.POST.get("post_type")
            goal = request.POST.get("goal")
            topic = request.POST.get("topic")
            des = request.POST.get("des")
            uuid = request.POST.get("uuid")
            
            is_image = True if pt == 'Image' else False
            
            clg = College.objects.get(uid = uuid)
            print("Generating ..")
            obj = SMCG(uid=uuid)
            responce = obj.get_content(request,platform=plt,type=pt,goal=goal,topic=topic,desc=des)
            context['output'] = responce
            context["image"] = is_image
            con = CONTENTS(clg=clg,
                            platform=plt,
                            post_type=pt,
                            goal=goal,
                            topic=topic,
                            desc=des,
                            responce=context['output'],
                            is_image=is_image)
            con.save()
            print("Is Image : ",is_image)
            if is_image is True:
                header = clg.banner.name
                header = os.path.join(settings.MEDIA_ROOT,header)
                out = generate_image(con.id,uuid,responce,des,header=header)
                print("Out : ",out)
                if out == True:
                    print("Image Saved")
                    context["image"] = CONTENTS.objects.get(id=con.id).output_image.url
                    print(context["image"])
                    print(context)
                else:
                    print("Image Not Saved")
                    context["image"] = False
                    
                

        except Exception as e:
            context['output'] = e
            context["image"] = False

    return JsonResponse(context)