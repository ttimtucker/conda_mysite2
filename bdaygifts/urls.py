from django.urls import path

from . import views
from covid import views as covid_views


urlpatterns = [
    path('tim/', views.tim, name='bdaygifts-tim'),
    path('karen/', views.karen, name='bdaygifts-karen'),
    path('', views.root, name='bdaygifts-root'),
    path('covid', covid_views.covid, name='covid')
]