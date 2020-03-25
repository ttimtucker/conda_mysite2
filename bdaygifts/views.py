from django.shortcuts import render
from django.http import HttpResponse
from bdaygifts.models import Gift


# Create your views here.

def tim(request):

    context={
        'gift': Gift.objects.all()
    }
    return render(request, 'bdaygifts/home.html', context)

def root(request):

    return render(request, 'bdaygifts/root.html')

def karen(request):

    context={
        'gift': Gift.objects.all()
    }
    return render(request, 'bdaygifts/home.html', context)

