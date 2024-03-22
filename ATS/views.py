import threading

from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .ats import run
import json
from django.conf import settings
import os

def ats(request):

    return  render(request,"ATS/ATS.html")


def ats_ev(request):

    context = {

    }

    if request.POST:
        uid = request.POST.get("uuid")
        jd = request.POST.get("jd")

        pdf = request.FILES.get("file")
        clg = College.objects.get(uid=uid)

        obj = ATS(college=clg,jd=jd,file=pdf,responce = "0")
        obj.save()
        media_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)

        obj.responce = run(clg.api_key,media_path,jd)
        context = json.loads(obj.responce)
        obj.save()

    return JsonResponse(context)