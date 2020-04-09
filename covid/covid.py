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
import globals
import pickle

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

    # webbrowser.open(r'file://{}'.format(os.path.abspath('covid.pdf')))
    # plt.clf()
    with open('fucking_globals','rb') as f:
        l=pickle.load(f)
    global_context=l[0]
    covid_url_choice=l[1]
    covid_url=l[2]
    #print('In plot_covid, dataset={}, global_context={}, covid_url={}'.format(dataset, global_context, covid_url))

    humdata_url = 'https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases'
    humdata_host = re.search(r'(^http[s]?:\/\/[\d\w\.]+)\/', humdata_url).group(1)
    country = 'US'
    csv_url = humdata_host + covid_url[dataset]
    title = dataset.split('.')[0]
    #print('title={}, csv_url={}'.format(title,csv_url))
    ylabel = re.search(r'^.*covid19_(.*)_.*', title).group(1)
    # print('csv_url={}'.format(csv_url))
    # urllib.request.urlretrieve(csv_url, 'covid.csv')
    df = pd.read_csv(csv_url)
    # df.head()
    df.to_csv('covid.csv', index=False)

    # print('Country entered is {}'.format(country))
    with open('covid.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        date_row = next(csv_reader)[4:]
        # print(date_row)
        ydata = []
        for row in csv_reader:
            if row[1] == country:
                ydata = list(map(int, row[4:]))
                # print('ydata={}'.format(ydata))
                break
        if not ydata:
            print('Could not find data for country {}'.format(country))

    dates = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in date_row]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ymin = min(ydata)
    ymax = max(ydata)
    # print(ymin,ymax)

    plt.locator_params(axis='y', nbins=10)
    custom_ticks = np.linspace(ymin, ymax, 20, dtype=int)
    # print(type(custom_ticks), custom_ticks)
    plt.gca().set_yticks(custom_ticks)
    plt.gca().set_yticklabels(custom_ticks)
    plt.plot_date(dates, ydata, xdate=True, marker=None, linestyle='solid')
    plt.gcf().autofmt_xdate()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.savefig('covid.pdf')
    webbrowser.open(r'file://{}'.format(os.path.abspath('covid.pdf')))
    plt.clf()

    return redirect('covid2')

    # return HttpResponse('This is where {} covid plot will happen'.format(dataset))

#   #country = input('Enter country: ')
#
# #while True:
#
#
#     dataset = int(input('Select a data set to plot: '))
#     if dataset:
#         print('Plotting dataset {} ({})'.format(dataset, covid_url_choice[dataset - 1]))
#         print('When finished with plot, close plot to display a different dataset')
#         # Get csv file
#         csv_url = humdata_host + covid_url[covid_url_choice[dataset - 1]]
#         title = covid_url_choice[dataset - 1].split('.')[0]
#         ylabel = re.search(r'^.*covid19_(.*)_.*', title).group(1)
#         # print('csv_url={}'.format(csv_url))
#         # urllib.request.urlretrieve(csv_url, 'covid.csv')
#         df = pd.read_csv(csv_url)
#         # df.head()
#         df.to_csv('covid.csv', index=False)
#
#         # print('Country entered is {}'.format(country))
#         with open('covid.csv') as csv_file:
#             csv_reader = csv.reader(csv_file)
#             date_row = next(csv_reader)[4:]
#             # print(date_row)
#             ydata = []
#             for row in csv_reader:
#                 if row[1] == country:
#                     ydata = list(map(int, row[4:]))
#                     # print('ydata={}'.format(ydata))
#                     break
#             if not ydata:
#                 print('Could not find data for country {}'.format(country))
#
#         dates = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in date_row]
#         plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
#         plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
#         ymin = min(ydata)
#         ymax = max(ydata)
#         # print(ymin,ymax)
#
#         plt.locator_params(axis='y', nbins=10)
#         custom_ticks = np.linspace(ymin, ymax, 20, dtype=int)
#         # print(type(custom_ticks), custom_ticks)
#         plt.gca().set_yticks(custom_ticks)
#         plt.gca().set_yticklabels(custom_ticks)
#         plt.plot_date(dates, ydata, xdate=True, marker=None, linestyle='solid')
#         plt.gcf().autofmt_xdate()
#         plt.title(title)
#         plt.xlabel("Date")
#         plt.ylabel(ylabel)
#         plt.savefig('covid.pdf')
#         webbrowser.open(r'file://{}'.format(os.path.abspath('covid.pdf')))
#        plt.clf()
#        return 0

    return redirect('covid2')