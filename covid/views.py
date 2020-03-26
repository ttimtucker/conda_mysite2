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

def ohiocovid(request):
    source = requests.get('https://coronavirus.ohio.gov/wps/portal/gov/covid-19/').text
    soup = BeautifulSoup(source, 'lxml')
    corona_dict={}
    for match in soup.find_all('div', class_='odh-ads__item'):
        #print('match=',match)
        title=match.find('div', class_='odh-ads__item-summary').text.strip()+":"
        #print('match2-1=',match2_unstripped)
        value=match.find('div', class_='odh-ads__item-title').text.strip()
        #print('match2-2=',match2_unstripped)
        corona_dict.update({title:value})
    #return HttpResponse("This is covid page")
    context={'dict': corona_dict}
    print('context=',context)
    return render(request, 'bdaygifts/covid.html', context)