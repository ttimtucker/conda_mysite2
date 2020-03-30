from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from bdaygifts.forms import FilterForm

# Create your views here.

def covid(request):


    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'html.parser')
    corona_dict={'callingviewkey':'covid'}
    for match in soup.find_all('div', id='maincounter-wrap'):
        corona_dict.update({match.h1.text.strip():match.div.text.strip()})
    #return HttpResponse("This is covid page")
    context={'dict': corona_dict}
    print('context=',context)
    return render(request, 'bdaygifts/covid.html', context)

def ohiocovid(request):
    source = requests.get('https://coronavirus.ohio.gov/wps/portal/gov/covid-19/').text
    soup = BeautifulSoup(source, 'html.parser')
    corona_dict={'callingviewkey':'ohiocovid'}
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

def selectregion(request):
    form=FilterForm(request.POST)
    #print('request.method=',request.method)
    #print('form before if=',form)
    #print('type form=',type(form))
    #print('xxx=',form['filter_by'])
    #print(dir(form['filter_by']))
    #print('dir form=',dir(form))
    if form.is_valid():
        print('valid form=',form.cleaned_data.get('filter_by'))
    else:
        print('form is not valid')
    selected=request.POST['dropdown'].strip()
    print('Region selected=',selected)
    if selected=='World':
        return covid(request)
    else:
        return ohiocovid(request)
    #return HttpResponse("This is selectregion page")