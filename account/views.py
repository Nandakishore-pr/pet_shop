from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from .forms import SignUpForm
from django.contrib.auth import login,authenticate,logout

from django.contrib import messages,auth

from account.models import User

import random

from .forms import SignUpForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

# Create your views here.

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # messages.success(request,'Account Created Successfully!!')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')


            request.session["username"] = username
            request.session["email"] = email
            request.session["password"] = password
            request.session["first_name"] = first_name
            request.session["last_name"] = last_name
            send_otp(request)
            return render(request,'account/otp.html',{"email":email})

          
        
    else: 
        form = SignUpForm()
    context = {
        'form':form
        }
    return render(request,'account/signup.html',context)



def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'nandakishore.p.r2002@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,'account/otp.html')



def  otp_verification(request):
    if  request.method=='POST':
        otp_=request.POST.get("otp")
    if otp_ == request.session["otp"]:
        encryptedpassword=make_password(request.session['password'])
        nameuser=User(username=request.session['username'],email=request.session['email'],password=encryptedpassword,first_name=request.session['first_name'],last_name=request.session['last_name'])
        nameuser.save()
        messages.info(request,'signed in successfully...')
        User.is_active=True 
        return redirect('account:login')
    else:
        messages.error(request,"otp doesn't match")
        return render(request,'account/otp.html')




@never_cache
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,'Hey, you are already logged in')
        return redirect("core:index")
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        
        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None :
            # if user.is_active:
            #     messages.warning(request, "your can't access ")
            # else:
            login(request, user)
            request.session['user_logged_in'] = True
            messages.success(request,'you have logged in')
            return redirect('core:index')
        else:
            messages.warning(request,'incorrect email or password')
    
    return render(request, 'account/login.html')


def logoutUser(request):
    logout(request)
    messages.success(request,f'You logged out')
    return redirect('core:index') 



def index(request):
    return render (request,'index.html')



