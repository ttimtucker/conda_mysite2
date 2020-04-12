import pandas as pd
import csv
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import datetime as dt
import numpy as np
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import os
import webbrowser
from django.http import HttpResponse
from django.shortcuts import redirect

#import globals
import pickle
from math import pow, modf, log10
import logging
from django.conf import settings
#from ..conda_mysite2.settings import STATICFILES_DIRS

plt.style.use('seaborn')
#humdata_host = re.search(r'(^http[s]?:\/\/[\d\w\.]+)\/', humdata_url).group(1)


def get_plot_choices():
    humdata_url = 'https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases'
    # Get html file from John Hopkins site
    try:
        source = requests.get(humdata_url).text
    except Exception as e:
        print(e)
        exit(1)

    soup = BeautifulSoup(source, 'html.parser')

    covid_url = {}
    for match in soup.find_all('div', class_='hdx-btn-group hdx-btn-group-fixed'):
        covid_url.update({match.a.span.text.strip(): match.a['href']})
    covid_url_choice = [i for i in list(covid_url.keys()) if i.find('iso') == -1 and i.find('narrow') == -1]
    # covid_url_choice=[ i for i in list(covid_url.keys()) ]
    # print(covid_url_choice)
    return [covid_url_choice, covid_url]

def plot_covid(dataset, global_context):
    logging.debug('in covid.covid.plot_covid')

    # webbrowser.open(r'file://{}'.format(os.path.abspath('covid.pdf')))
    # plt.clf()
    with open('/tmp/fucking_globals','rb') as f:
        l=pickle.load(f)
    global_context=l[0]
    covid_url_choice=l[1]
    covid_url=l[2]
    #print('In plot_covid, dataset={}, global_context={}, covid_url={}'.format(dataset, global_context, covid_url))

    humdata_url = 'https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases'
    humdata_host = re.search(r'(^http[s]?:\/\/[\d\w\.]+)\/', humdata_url).group(1)
    country = 'US'
    csv_url = humdata_host + covid_url[dataset]
    title = 'COVID-19 data compiled by John Hopkins University\nDataset={}\nCountry={}'.format(dataset.split('.')[0],country)
    print('title={}, csv_url={}'.format(title,csv_url))
    ylabel = country+' '+re.search(r'^.*covid19_(.*)_.*', dataset.split('.')[0]).group(1).capitalize()
    # print('csv_url={}'.format(csv_url))
    # urllib.request.urlretrieve(csv_url, '/tmp/covid.csv')
    df = pd.read_csv(csv_url)
    # df.head()
    df.to_csv('/tmp/covid.csv', index=False)

    # print('Country entered is {}'.format(country))
    with open('/tmp/covid.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        date_row = next(csv_reader)[4:]
        # print(date_row)
        ydata = []
        for row in csv_reader:
            if row[1] == country:
                ydata = list(map(int, row[4:]))
                print('ydata={}'.format(ydata))
                break
        if not ydata:
            print('Could not find data for country {}'.format(country))

    dates = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in date_row]
    logging.debug('dates=%s',dates)

    fig,ax=plt.subplots()
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ymax = max(ydata)

    yupper=int(pow(10,int(modf(log10(ymax))[1]))*(int(pow(10,modf(log10(ymax))[0]))+1))
    custom_ticks = np.linspace(0, yupper, 11, dtype=int)
    fig.gca().set_yticks(custom_ticks)
    fig.gca().set_yticklabels(custom_ticks, color='green')
    ax.plot_date(dates, ydata, xdate=True, marker=None, linestyle='solid', linewidth=2, color='black')
    plt.gcf().autofmt_xdate()
    ax.tick_params(axis="y", labelsize=10, colors='blue')
    ax.tick_params(axis="x", labelsize=10, colors='blue')
    plt.title(title)
    #plt.xlabel("Date")
    plt.ylabel(ylabel, fontname="Arial", fontsize=12 )
    plt.tight_layout()

    #plt.savefig('/home/ttucker/conda_mysite2/static/covid/covid.png')
    plot_url=settings.STATICFILES_DIRS[0]+'/covid/covid.png'
    plt.savefig(plot_url)
    #webbrowser.open(r'file://{}'.format(os.path.abspath('/tmp/covid.png')))
    #plt.clf()

    #return redirect('covid2')
    return 'covid/covid.png'
