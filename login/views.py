from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm

from django.contrib import messages
from .forms import *

#start of libraries for registration and login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout#for login and logout- and authentication
#end of libraries for registration and login


# Create your views here.
def registerpage(request):
    title="User registeration"
    if request.user.is_authenticated:
        return redirect("allifmaalapp:allifmaalmaindashboard")
    else:
        register_form=CreateUserForm()
        if request.method=='POST':
            register_form=CreateUserForm(request.POST)
            if register_form.is_valid():
                user=register_form.save()
            
                username=register_form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ username)
            
                return redirect('login:loginpage')
    
    context={
        "title":title,
        "register_form":register_form,  
    }
    return render(request,"register/register.html",context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    
    else:
        form=AddUserDetailsForm
        if request.method=='POST':
        
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:#if there is an authenticated user
                login(request, user)
                return redirect('allifmaalapp:allifmaalmaindashboard')
            else:
                messages.info(request,'Dear '+username + ', Your username or password is incorrect ! ')
                form=AuthenticationForm(request)
    context={"form":form,
        
        }
    return render(request,'login/login.html',context)


def logoutpage(request):
    logout(request)#logs user out
    messages.success(request,"Successfully logged out ")
    return redirect('login:loginpage')


def systemUserProfile(request):
   

    mycontext={
        
    }
    return render(request,'profile/userProfile.html',mycontext)

def editProfile(request):
    title="Edit profile"
    #editForm=UserChangeForm(instance=request.user)
    editForm=UserEditForm(instance=request.user)
    if request.method=='POST':
        editForm=UserEditForm(request.POST or None, instance=request.user)
        if editForm.is_valid():
            editForm.save()
           
            return redirect('website:website')
    
    context={
        "title":title,
        "editForm":editForm,  
    }
    return render(request,"profile/editprofile.html",context)


