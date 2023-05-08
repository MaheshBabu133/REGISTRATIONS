from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.
from app.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid username or password')
        
    return render(request,'user_login.html')





def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))











@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('change_password is successfull')
    return render(request,'change_password.html')



def forget_password(request):
    if request.method=='POST':
        username=request.POST['username']
        pw=request.POST['pw']
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('<h1>Password change successfully</h1>')
    return render(request,'forget_password.html')





def registrations(request):
    UO=UserForm()
    PO=ProfileForm()
    d={'UO':UO,'PO':PO}
    if request.method=='POST' and request.FILES:
        UFO=UserForm(request.POST)
        PFO=ProfileForm(request.POST,request.FILES)
        if UFO.is_valid() and PFO.is_valid():
            NUFO=UFO.save(commit=False)
            password=UFO.cleaned_data['password']
            NUFO.set_password(password)
            NUFO.save()
            NPFO=PFO.save(False)
            NPFO.username=NUFO
            NPFO.save()
            send_mail('registartion',
                      'suuccessful',
                      'maheshbabuntr123@gmail.com',
                      [NUFO.email],
                      fail_silently=True)
            
            return HttpResponse('<h1>Registartion done successfully</h1>')
        else:
            return HttpResponse('<h1>data is valid</h1>')
    return render(request,'registrations.html',d)