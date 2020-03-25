from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#from .forms import RegistrationForm
from webapp3.forms import RegistrationForm

def index(request):
    #return HttpResponse("<H2> Hey, welcome to Django tutorial webapp3</H2>")
    form=RegistrationForm()
    context={
        "myregistrationform": form
    }
    return render(request,'webapp3/index.html',context)
