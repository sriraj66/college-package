from django.shortcuts import render, redirect, get_object_or_404
from authentication.views import load_config
from django.contrib.auth.decorators import login_required
from .utils import MockInter
from django.http import HttpRequest, HttpResponse, JsonResponse
import json
from .models import *
from django.contrib.messages import success
import logging

home = "mockinterview/"

# Set up logging
logger = logging.getLogger(__name__)

def index(request):
    context = load_config(request)
    
    if request.method == 'POST':
        res = request.FILES.get('resume')
        return redirect("process")
    
    user = request.user 
    all_interviews = CreateInterview.objects.all()
    user_interviews = [interview for interview in all_interviews if interview.user_interview(user)]

    context['interviews'] = user_interviews
    
    return render(request, home + "index.html", context=context)

@login_required
def process(request: HttpRequest, id: int) -> HttpResponse:
    context = load_config(request)
    
    key = context['profile'].college.api_key
    
    interview_check = get_object_or_404(CreateInterview, id=id)
    context['id'] = id
    interview = get_object_or_404(interview_check.attendence, user=request.user)
    
    if 'messages' in request.session:
        iter = MockInter(key=key, role="Django Developer", messages=request.session['messages'])
    else:
        iter = MockInter(key=key, role="Django Developer")
        request.session['messages'] = iter.messages
    
    if request.method == 'POST':
        text = request.POST.get('transcription', 'No Answer')
        res = iter.make_con(text)
    else:
        res = iter.make_con(None)
    
    request.session['messages'] = iter.messages
    try:
        context['response'] = json.loads(res)
    except json.JSONDecodeError:
        logger.error(f"JSON decoding error for response: {res}")
        context['response'] = {"error": "Failed to parse the response."}
    
    if context['response'].get('is_ended'):
        interview.conversation = request.session['messages']
        interview.result = json.dumps(context['response']) 
        if 'messages' in request.session:
            del request.session['messages']
        interview.is_ended = True
        interview.save()
        return redirect("process_result", interview.id)
    
    interview.conversation = request.session['messages']
    interview.save()
    return render(request, home + "_.html", context=context)

@login_required
def process_result(request, id):
    context = load_config(request)
    
    interview = get_object_or_404(InterviewResult, id=id)
    try:
        data = json.loads(interview.result)
    except json.JSONDecodeError:
        logger.error(f"JSON decoding error for interview result with id {id}: {interview.result}")
        data = {"error": "Invalid interview result data."}
    
    context['result'] = data
    print(data)
    context['starts'] = range(0, int(data.get('rating', 0)))
    return render(request, home + "result.html", context=context)

@login_required
def interview_check(request, id):
    context = load_config(request)
    user = request.user
    
    interview = get_object_or_404(CreateInterview, id=id)
    context['interview'] = interview
    if request.method == 'POST':
        if interview.user_interview(user):
            if interview.attendence.filter(user=user).exists():
                success(request, 'You already attended this interview!!', extra_tags='info')
                intRes = interview.attendence.get(user=user)
                request.session['messages'] = intRes.conversation
                if intRes.is_ended:
                    return redirect("process_result", intRes.id)
            else:
                intRes = InterviewResult(user=user)
                
                intRes.save()
                if 'messages' in request.session:
                    del request.session['messages']
                interview.attendence.add(intRes)
                interview.save()
            return redirect('process', interview.id)
        else:
            success(request, 'You are not allowed to Attend', extra_tags='danger')
            return redirect('mi')
    
    return render(request, home + "check.html", context=context)
