from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from app.forms import *
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
            return HttpResponse('<h1>Registartion done successfully</h1>')
        else:
            return HttpResponse('<h1>data is valid</h1>')
    return render(request,'registrations.html',d)