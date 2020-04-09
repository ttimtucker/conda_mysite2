from django.urls import path

from . import views
from covid import views as covid_views


urlpatterns = [
    path('tim/', views.tim, name='bdaygifts-tim'),
    path('karen/', views.karen, name='bdaygifts-karen'),
    path('', views.root, name='bdaygifts-root'),
    path('covid2/', covid_views.covid2, name='covid2'),
    #path('ohiocovid/', covid_views.ohiocovid, name='ohiocovid'),
    path('selectregion/', covid_views.selectregion, name='selectregion'),
    path('selectplot/', covid_views.selectplot, name='selectplot')
]