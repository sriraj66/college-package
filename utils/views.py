from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from authentication.views import load_config
from .forms import *
from django.contrib.messages import *
import pandas as pd


@login_required
def my_profile(request):
    context = load_config(request)
    
    
    return render(request,'utils/profile.html',context)

def edit_profile(request):
    context = load_config(request)
    context['complete_triger'] = False
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES,instance=context['profile'])
        if form.is_valid():
            phone = form.cleaned_data['phone']
            gender = form.cleaned_data['gender']
            if len(phone) !=10 or gender == 'None':
                error(request,"Please Enter The valid Mobile Number or Gender !!",extra_tags='danger')
                return redirect('edit_profile')
            else:
                form.save()
            

            return redirect('my_profile')
    else:
        form = StudentProfileForm(instance=context['profile'])
    
    context['form'] = form
    
    return render(request,'utils/edit_profile.html',context)


@login_required
def load_student(request):
    context = load_config(request)    
    if not request.user.is_superuser and not context['profile'].is_admin:
        return redirect("err","Not Authorized !!")
    
    if request.POST:
        try:
            file = request.FILES.get("exel")
            
            df = pd.read_excel(file)
            
            for index, row in df.iterrows():
                try:
                    user = User(
                        username = row['email'],
                        email = row['email'],
                        first_name = row['first_name'],
                        last_name = row['last_name'],
                    )
                    user.set_password(raw_password='Student@123')
                    
                    user.save()
                    
                    
                    profile = Students.objects.get(user=user)
                    profile.degree = row['degree']
                    profile.branch = row['branch']
                    profile.roll = row['roll_num']
                    profile.phone = row['phone']
                    g = row['gender'].lower()
                    
                    if g == 'm' or g == 'male':
                        profile.gender = 'Male'
                    elif g == 'f' or g == 'female':
                        profile.gender = 'Female'
                    else:
                        profile.gender = 'None'
                    
                    profile.college = context['profile'].college
                    profile.save()
                    context['profile'].college.students.add(profile)
                    context['profile'].college.save()
                except Exception as e:
                    print("Error saving profile")
                    continue    
                
            success(request,"Students List Sucessfullt Loded Password : Student@123")
            return redirect("my_students")
        except Exception as e:
            success(request,e,extra_tags="danger")
            
    
    return render(request,'utils/load_students.html',context)
    
def my_students(request):
    context = load_config(request)
    
    if not request.user.is_superuser and not context['profile'].is_admin:
        return redirect("err","Invalid Access!!")
    
    try:
        context['records'] = CollegeAdmin.objects.get(user=request.user).students.all()
        print(context)
    except Exception as e:
        return redirect("err", e)
    return render(request,'utils/students.html',context)


@login_required
def my_staffs(request):
    context = load_config(request)
    
    if not request.user.is_superuser and not context['profile'].is_admin:
        return redirect("err","Invalid Access!!")
    
    try:
        context['records'] = CollegeAdmin.objects.get(user=request.user).staffs.all()
        print(context)
    except Exception as e:
        return redirect("err", e)
    return render(request,'utils/students.html',context)



@login_required
def load_staffs(request):
    context = load_config(request)    
    if not request.user.is_superuser and not context['profile'].is_admin:
        return redirect("err","Not Authorized !!")
    
    if request.POST:
        try:
            file = request.FILES.get("exel")
            
            df = pd.read_excel(file)
            
            for index, row in df.iterrows():
                try:
                    user = User(
                        username = row['email'],
                        email = row['email'],
                        first_name = row['first_name'],
                        last_name = row['last_name'],
                    )
                    user.is_staff = True
                    user.set_password(raw_password='Staff@123')
                    
                    user.save()
                    
                    
                    profile = Staffs.objects.get(user=user)
                    profile.degree = row['degree']
                    profile.branch = row['branch']
                    profile.roll = row['roll_num']
                    profile.phone = row['phone']
                    g = row['gender'].lower()
                    
                    if g == 'm' or g == 'male':
                        profile.gender = 'Male'
                    elif g == 'f' or g == 'female':
                        profile.gender = 'Female'
                    else:
                        profile.gender = 'None'
                    
                    profile.college = context['profile'].college
                    profile.save()
                    context['profile'].college.staffs.add(profile)
                    context['profile'].college.save()
                    
                except Exception as e:
                    print("Error saving profile : ",e)
                    continue    
                
            success(request,"Staff List Sucessfullt Loded Password : Staff@123")
            return redirect("my_staffs")
        except Exception as e:
            success(request,e,extra_tags="danger")
            
    
    return render(request,'utils/load_staff.html',context)
    