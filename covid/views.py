from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

# Create your views here.

def covid(request):
    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'lxml')
    corona_dict={}
    for match in soup.find_all('div', id='maincounter-wrap'):
        corona_dict.update({match.h1.text.strip():match.div.text.strip()})
    #return HttpResponse("This is covid page")
    context={'dict': corona_dict}
    print('context=',context)
    return render(request, 'bdaygifts/covid.html', context)
