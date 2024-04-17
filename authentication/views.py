from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.messages import success,error,warning
from django.contrib.auth.decorators import login_required 
from utils.models import Students,Staffs


def load_config(request):
    try:
        if request.user.is_staff or request.user.is_superuser:
            profile = Staffs.objects.get(user=request.user)
        else:
            profile = Students.objects.get(user=request.user)
        
        context = {
            'profile': profile
        }
        
        return context
    except Exception as e:
        print(e)
        return {}
        
def login_view(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                success(request,f"Successfully logged in as {username}.")
                return redirect('index')
            else:
                warning(request,f"Invalid username or password!!")
                return redirect('login')
        except Exception as e:
            error(request,f"Error while logging in!!",extra_tags="danger")
            pass
    
    return render(request, 'auth/login.html',context)


def log_out(request):
    logout(request)
    return redirect("index")