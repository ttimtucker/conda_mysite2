from django.shortcuts import render
from django.http import HttpResponse
from bdaygifts.models import Gift
import logging

logger=logging.getLogger(__name__)
logging.basicConfig(filename='/tmp/example.log',level=logging.DEBUG)

logger.debug("Logging Test!!")

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

def games(request):
    #print('Executing "games" in {} '.format(__name__))
    context={
        'gift': Gift.objects.all()
    }

    return render(request, 'bdaygifts/home.html', context)
