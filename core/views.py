from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import *
from .utils import *
from .embed import *
import threading
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.templatetags.static import static

def index(request):
    context = {
      "college":College.objects.all(),
    }
    if request.POST:
        uid = request.POST.get('uid')
        prompt = request.POST.get('prompt')
        print(prompt,uid)
        
        emb = Emmbedded(uid=uid, prompt=prompt)
        responce = emb.query()
        print(responce)
        
    return render(request,'chatbot/chat.html',context)


def college_form(request):
    if request.method == 'POST':
        form = CollegeForm(request.POST)
        if form.is_valid():
            mid = form.save()
            root_url = form.cleaned_data['root_url']
            
            start_page_source(mid.id)
            
            return redirect('source_code',mid.uid)  
    else:
        form = CollegeForm()
    return render(request, 'chatbot/college.html', {'form': form})

def source_code(request,uuid):
    
    context = {}
    clg = College.objects.get(uid=uuid)
    stylesheet  = request.build_absolute_uri(static('css/style.css'))
    script1  = request.build_absolute_uri(static('js/service.js'))
    script2  = request.build_absolute_uri(static('js/script.js'))
    
    domain = request.build_absolute_uri('/')
    url_path = reverse('api_get_responce')
    full_url = f'{domain.rstrip("/")}{url_path}'
    print(full_url)
    code = f"""
  <link rel="stylesheet" href="{stylesheet}">
  
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script>
  const URL = '{full_url}'
  </script>
  <button class="btn-pop-message" onclick="toggleMessage()"><span><i class="fas fa-close"></i></span></button>

  <section class="msger --hide" id="msger">
    <header class="msger-header">
      <div class="msger-header-title">
        <i class="fas fa-comment-alt"></i> {clg.name}
      </div>
      <div class="msger-header-options" onclick="toggleMessage()">
        <span><i class="fas fa-times"></i></span>
      </div>
    </header>

    <main class="msger-chat">

    </main>

    <form class="msger-inputarea">
      <input type="text" name='query' class="msger-input" placeholder="Enter your message...">
      <input type="text" name='uuid' value='{uuid}' hidden class="msger-uuid"">

  <button type=" submit" class="msger-send-btn">Send</button>
    </form>
  </section>
  <script src="{script1}"></script>
  <script src="{script2}"></script>
  <script src='https://use.fontawesome.com/releases/v5.0.13/js/all.js'></script>
    """
    context['code'] = code
    return render(request,'chatbot/source_code.html',context)

@csrf_exempt
@api_view(['POST'])
def get_chat_responce(request):
    responce = {
        "status": 403,
        "request" : "",
        "response" :"",
        "updated":"",
        "profile_url":"",
        "name":"",
        "time":"",
        "error":False
    }
    
    if request.method == 'POST':
        uid = request.POST.get('uuid')
        query = request.POST.get('query')
        print("UUID : ",uid)
        print("QUERY : ",query)
        clg = College.objects.get(uid=uid)
        print(clg.name)
        responce['name'] = clg.name
        responce['profile_url'] = clg.logo
        print(responce['profile_url'])
        responce['updated'] = clg.updated.date()
        try:
            obj = Emmbedded(uid=uid,prompt=query)
            responce['response'] = obj.query()
            msg = Messages(to=clg,request=query,responce=responce['response'])
            msg.save()
            responce['time'] = msg.created.time()
            responce['status'] = 200
        except Exception as e:
            responce['response'] = str(e)
            responce['error'] = True
        
        
    return JsonResponse(responce)
