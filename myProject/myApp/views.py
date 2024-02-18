from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib import messages

from django.contrib.auth import get_user_model
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from datetime import date
from django.db.models import Q
from myProject.settings import EMAIL_HOST_USER
import random 
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string



def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('mySigninPage')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('mySigninPage')


def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')


def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('mySigninPage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signupPage.html', {'form': form})


def mySigninPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboardPage')
    else:
        form = AuthenticationForm()
    return render(request, 'loginPage.html', {'form': form})


def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('mySigninPage')

def dashboardPage(request):
    user = userProfile.objects.filter()
    return render(request, 'dashboardPage.html', {'user':user})

def forget_pass(request):
    if request.method == 'POST':
        my_email = request.POST.get('email')
        user = Custom_User.objects.get(email = my_email)
        otp = random.randint(1111111,999999999)
        user.otp_token = otp
        user.save()

        sub = f""" Your Otp : {otp}"""
        msg = f" Your otp is {otp}, Keep it secret"
        from_mail = EMAIL_HOST_USER
        receipent = [my_email]

        print(user)
        print(receipent)
        print(from_mail)

        send_mail(
            subject=sub,
            recipient_list=receipent,
            from_email= from_mail,
            message=msg,
        )
        return redirect('update_pass')
    return render(request, 'forgetpass.html')

def update_pass(request):
    if request.method=="POST":
        mail = request.POST.get('email') 
        otp = request.POST.get('otp') 
        password = request.POST.get('password') 
        c_password = request.POST.get('c_password') 
        
        print(mail,otp,password,c_password)

        user = Custom_User.objects.get(email=mail)
        print(user)
        if user.otp_token!= otp :
            return redirect('forget_pass')
        
        if password!= c_password:
            return redirect('forget_pass')
        
        user.set_password(password) 
        user.otp_token = None 
        user.save()
        print(user)
        return redirect ('mySigninPage')

    return render(request, 'updatepass.html')


def createateProfile(request):
    profile_user=0
    try:
        profile_user=userProfile.objects.get(user=request.user)
        
    except:
        pass
    if request.method=='POST' and profile_user:
        form = userProfileForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()

            return redirect('dashboardPage')
    elif request.method=='POST':
        form = userProfileForm(request.POST, request.FILES)

        if form.is_valid():
            co=form.save(commit=False)
            co.user=request.user
            co.save()
            return redirect('dashboardPage')
        
    elif profile_user:
        form=userProfileForm(instance=profile_user)
    else:
        form=userProfileForm()
    return render(request, 'profile.html', {'form':form, 'profile_user':profile_user})


def editProfile(request):
    profile_user=0
    try:
        profile_user=userProfile.objects.get(user=request.user)
    except:
        pass
    if request.method=='POST':
        form = userProfileForm(request.POST,instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect('dashboardPage')
        
    else:
        form=userProfileForm(instance=profile_user)
    return render(request, 'profile.html', {'form': form})


def deleteprofile(request, id):
    user=userProfile.objects.get(id=id)
    user.delete()
    return redirect('createateProfile')


def items(request):
    if request.method=="POST":
        form=itemsallForm(request.POST)
        if form.is_valid():
            co=form.save(commit=False)
            co.user=request.user
            co.save()
            return redirect('vieweatinglist')
    else:
        form=itemsallForm()
    return render(request, 'calorieitem.html', {'form':form})

def vieweatinglist(request):
    items = itemsall.objects.all()  
    return render(request, 'viewlist.html', {'items': items})


def edititem(request, id):
    item=itemsall.objects.get(id=id)
    if request.method=='POST':
        form=itemsallForm(request.POST,instance=item)
        if form.is_valid():
            co=form.save(commit=False)
            co.user=request.user
            co.save()
            return redirect('vieweatinglist')
    else:
        form=itemsallForm(instance=item)
    return render(request, 'calorieitem.html', {'form':form})

def deleteitem(request, id):
    item=itemsall.objects.get(id=id)
    item.delete()
    return redirect('vieweatinglist')


def profilePage(request):
    user = request.user
    msg=0
    info=0
    BMR = 0
    try:
        info= userProfile.objects.get(user = user)

        if info.gender == "male":
            BMR = 66.47 + (13.75*info.weight) + (5.003*info.height) - (6.755*info.age)
        else:
            BMR = 655.1 + (9.563*info.weight) + (1.850*info.height) - (4.676*info.age)

        info.BMR = BMR 
        info.save()
    except:
        msg= "Please Update Your Profile First"

    return render(request,"profilepage.html",{'info':info,'msg':msg, 'BMR':BMR})


def helloPage(request):
    date = 0
    sum = 0
    info = 0
    n_t_c = 0
    user = request.user
    info= userProfile.objects.get(user = user)
    item_list = itemsall.objects.filter(user=user)
    if request.method == "POST":
        date = request.POST.get('date')
        filterd_list = item_list.filter(date=date)
        
        for i in filterd_list:
            sum += i.calorie_consumed

    n_t_c = info.BMR - sum
    
    return render(request, "hello.html", {'sum':sum, 'info':info,'n_t_c':n_t_c})