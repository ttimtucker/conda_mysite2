from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .forms import RegistrationForm


def index(request):
    #return HttpResponse("<H2> Hey, welcome to Django tutorial</H2>")
    form=RegistrationForm()
    context={
        "myregistrationform": form
    }
    return render(request,'webapp2/index.html',context)