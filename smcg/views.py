from django.shortcuts import render
from core.constants import *
from django.http import JsonResponse
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
