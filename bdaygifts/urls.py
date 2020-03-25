from django.urls import path

from . import views


urlpatterns = [
    path('tim/', views.tim, name='bdaygifts-tim'),
    path('karen/', views.karen, name='bdaygifts-karen'),
    path('', views.root, name='bdaygifts-root')
]