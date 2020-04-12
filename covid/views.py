from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from bdaygifts.forms import FilterForm, PlotForm
from covid.covid import get_plot_choices, plot_covid
import re
from django import forms
import pickle
import logging

# Create your views here.

def covid2(request):

    logging.debug('in covid.views.covid2')
    l=get_plot_choices()
    covid_url_choice=l[0]
    covid_url = l[1]
    Filter_Choices=[ [covid_url_choice[i], re.search(r'covid19_(.*)_', covid_url_choice[i]).group(1) ] for i in range(len(covid_url_choice))]
    global_context={'key': Filter_Choices}
    logging.debug('covid.views.covid2: global_context=%s', global_context)
    with open('/tmp/fucking_globals', 'wb') as f:
        pickle.dump([global_context,covid_url_choice,covid_url],f)
    return render(request, 'bdaygifts/covid2.html', global_context)


def selectplot(request):
    logging.debug('in covid.views.selectplot')
    form=PlotForm(request.POST)
    selected=request.POST['dropdown'].strip()
    #print('Region selected=',selected)
    with open('/tmp/fucking_globals','rb') as f:
        l=pickle.load(f)
    global_context=l[0]
    cplot_filename=plot_covid(selected, global_context)
    logging.debug('in covid.views.selectplot: plot file = %s', cplot_filename)
    #return plot_covid(selected, global_context)
    #return redirect('covid2')
    dict={'plot':{'plot': 'covid/covid.png'}}
    return render(request, 'bdaygifts/covid_plot.html', dict)


def selectregion(request):
    form=FilterForm(request.POST)
    #print('request.method=',request.method)
    #print('form before if=',form)
    #print('type form=',type(form))
    #print('xxx=',form['filter_by'])
    #print(dir(form['filter_by']))
    #print('dir form=',dir(form))
    if form.is_valid():
        logging.debug('valid form=')
    else:
        logging.debug('form is not valid')
    selected=request.POST['dropdown'].strip()
    #print('Region selected=',selected)
    if selected=='World':
        return covid(request)
    else:
        return ohiocovid(request)
    #return HttpResponse("This is selectregion page")


# def covid(request):
#
#
#     source = requests.get('https://www.worldometers.info/coronavirus/').text
#     soup = BeautifulSoup(source, 'html.parser')
#     corona_dict={'callingviewkey':'covid'}
#     for match in soup.find_all('div', id='maincounter-wrap'):
#         corona_dict.update({match.h1.text.strip():match.div.text.strip()})
#     #return HttpResponse("This is covid page")
#     context={'dict': corona_dict}
#     print('context=',context)
#     return render(request, 'bdaygifts/covid.html', context)
#
# def ohiocovid(request):
#     source = requests.get('https://coronavirus.ohio.gov/wps/portal/gov/covid-19/').text
#     soup = BeautifulSoup(source, 'html.parser')
#     corona_dict={'callingviewkey':'ohiocovid'}
#     for match in soup.find_all('div', class_='odh-ads__item'):
#         #print('match=',match)
#         title=match.find('div', class_='odh-ads__item-summary').text.strip()+":"
#         #print('match2-1=',match2_unstripped)
#         value=match.find('div', class_='odh-ads__item-title').text.strip()
#         #print('match2-2=',match2_unstripped)
#         corona_dict.update({title:value})
#     #return HttpResponse("This is covid page")
#     context={'dict': corona_dict}
#     print('context=',context)
#     return render(request, 'bdaygifts/covid.html', context)
