from django.shortcuts import render
from smcg.constants import *
from django.http import JsonResponse
from smcg.smcg import *
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

# to do ajax

def gen_smcg(request):
    context = {
        "output":"No Output"
    }
    if request.POST:
        try:
            plt = request.POST.get("platform")
            pt = request.POST.get("post_type")
            goal = request.POST.get("goal")
            topic = request.POST.get("topic")
            des = request.POST.get("des")
            uuid = request.POST.get("uuid")
            print(uuid)
            obj = SMCG(uid=uuid)
            responce = obj.get_content(request,platform=plt,type=pt,goal=goal,topic=topic,desc=des)
            print(responce)
            context['output'] = responce
        except Exception as e:
            context['output'] = e

    return JsonResponse(context)