from django.shortcuts import render,redirect
from django.http import JsonResponse
from authentication.views import load_config
from django.contrib.auth.decorators import login_required
from .models import Form,Response,Questions,Analysis_with_exel
from feed360 import models
from .forms import *
from django.contrib.messages import success,error,warning
# QR
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import pandas as pd
from .analysis import Analysis

def generate_qr_image(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='#892cdc', back_color='white')
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return ContentFile(img_io.getvalue())


def form_to_df(form_id):
    form = Form.objects.get(id=form_id)
    questions = form.questions.all()
    responses = form.responses.all()
    headers = [question.question for question in questions]
    data = {}
    
    for i in headers:
        data[i] = []
    
    for i in responses:
        data[i.question.question].append(i.response)
    
    df = pd.DataFrame.from_dict(data)
    return df
    

@login_required
def feed360(request):
    context = load_config(request)
    if not request.user.is_staff:
        return redirect("err","Access Restricted!!")
    
    if request.POST:
        
        form = Form(staff = context['profile'])
        form.save()
        
        return redirect("create_form",form.id)
    
    context['records'] = Form.objects.filter(staff=context['profile'])
    context['ExelForm'] = Analysis_with_exel.objects.filter(staff=context['profile'])
    
    return render(request, 'feed360/feed360.html',context)

@login_required
def create_form(request,id):
    
    context = load_config(request)
    if not request.user.is_staff:
        return redirect("err","Access Restricted!!")
    
    form = Form.objects.get(id=id)
    context['form'] = form
    context['questions'] = form.questions.all()
    context['responses'] = form.responses.all()
    
    domain = request.build_absolute_uri('/')
    url_path = form.get_absolute_url()
    full_url = f'{domain.rstrip("/")}{url_path}'
    context['full_url'] = full_url
    if not form.qr:
        qr = generate_qr_image(full_url)
        
        form.qr.save(f"QR{form.id}.jpg",qr)
        success(request,"Qr Generated !!")
        
    if request.POST:
        name = request.POST.get("name",f"untitled_{form.id}")
        form.name = name
        form.save()
    
    return render(request, 'feed360/createform.html',context)

@login_required
def create_question(request,id):
    print("Callse")
    context = load_config(request)
    if not request.user.is_staff:
        return redirect("err","Access Restricted!!")
    model = Form.objects.get(id=id)
    
    if request.POST:
        form = QuestionsForm(request.POST,user = context['profile'],form=model)
        if form.is_valid():
            qus = form.save()
            
            model.questions.add(qus)
            model.save()
            success(request,"Question Added to the Form!!")
        else:
            error(request,"Form is Invalid!!",extra_tags="danger")
            
        return redirect('create_form',id)
    else:
        context['form'] = QuestionsForm(user = context['profile'],form=model)
        context['form_id'] = id or 0
    return render(request, 'feed360/createquestion.html',context)

@login_required
def edit_question(request,id):
    context = load_config(request)
    ques = Questions.objects.get(id=id)
    
    if not request.user.is_staff and context['profile'] == ques.staff:
        return redirect("err","Access Restricted!!")
    if request.POST:
        form = QuestionsForm(request.POST,user = context['profile'],instance=ques,form=ques.form_id)
        if form.is_valid():
            qus = form.save()
            
            success(request,"Question Saved !!")
        else:
            error(request,"Form is Invalid!!",extra_tags="danger")
            
        return redirect('create_form',ques.form_id.id)
    else:
        context['form'] = QuestionsForm(instance=ques,user = context['profile'],form=ques.form_id)
        context['form_id'] = id or 0
    
    return render(request, 'feed360/createquestion.html',context)

@login_required
def delete_question(request,id):
    context = load_config(request)
    ques = Questions.objects.get(id=id)
    form_id = ques.form_id.id
    
    if not request.user.is_staff and context['profile'] == ques.staff:
        return redirect("err","Access Restricted!!")
    
    ques.delete()
    success(request,"Question Deleted !!")
    
    return redirect("create_form",form_id)

@login_required
def view_form(request,id):
    context = load_config(request)
    
    form = Form.objects.get(id=id)
    
    
    if (request.user.is_staff and context['profile'] == form.staff) or request.user.is_staff is False:
        context['form'] = form
        
        questions = form.questions.all()
        context['questions'] = questions
        
        if request.POST and not request.user.is_staff:
            field_labels = [[f"response{i.id}",i.field_type,i.id] for i in questions]
            
            for i in field_labels:
                ans = request.POST.get(i[0])
                if i[1] == 'Rating':
                    ans = int(ans)
                    if ans>=6 or ans<0:
                        ans = 0
                    rating_context = ['Needs Improvement','Needs Some Improvements',"Meets Expectations","Very Satisfactory","Exceeds Expectations"]
                    ans = rating_context[ans-1]
                    
                res = Response(
                    student = context['profile'],
                    question = Questions.objects.get(id=i[2]),
                    response = ans,
                    form_id = form,
                )
                res.save()
                form.responses.add(res)
                form.save()
            
            success(request,"Form Has been Submited!!")
            return redirect("index")
        
    else:
        return redirect("err","Access Restricted!!")
    
    
    return render(request, 'feed360/viewform.html',context=context)

@login_required
def delete_form(request,id):
    cotnext = load_config(request)
    if not request.user.is_staff:
        return redirect("err","Access Restricted!!")
    try:
        form = Form.objects.get(id=id)
        
        if request.POST and cotnext['profile'] == form.staff:
            
            form.delete()
            
            warning(request,"Form Has been Deleted!!")
            return redirect("feed360")
            
    except Exception as e:
        return redirect("err","Access Restricted!!")
        
    return redirect("create_form",id)

def sentimental_analysis(request,id):
    context = {
        "output":"",
        "error":"",
    }
    
    if not request.user.is_staff:
        error(request,"Invalid User!")
        return redirect("create_form",id)
    if request.POST:
        try:
            df = form_to_df(id)    
            ana = Analysis(id,df)
            responce = ana.analysis()
            context["output"] = responce
            form = Form.objects.get(id=id)
            ana = models.Analysis(form_id=form,report=str(responce))
            ana.save()
            form.analysis.add(ana)
            form.save()
            
            config = load_config(request)
            config['profile'].reduce_credits(3)
            
                
        except Exception as e:
            success(request,str(e),extra_tags="danger")
            context["error"] = e
    else:
        return redirect('err',"Invalid Request!")
    
    
    return JsonResponse(context)


@login_required
def analysis_with_exel(request):
    context = load_config(request)

    if request.POST:
        file = request.FILES.get("exel")
        
        df = pd.read_excel(file)
        df = df.dropna(axis=1, how='all')
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        obj = Analysis_with_exel(
            staff = context['profile'],
            file = file,
        )
        obj.save()
        
        ana = Analysis(id=obj.id,df=df,file=True)
        
        obj.report = ana.analysis()
        obj.save()
        success(request,"Analysis Done !")
        context['profile'].reduce_credits(4)

        
    else:
        success(request,"Invalid Request !!",extra_tags="danger")
    
    return redirect("feed360")
