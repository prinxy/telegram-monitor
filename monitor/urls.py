from django.urls import path
from django.conf import settings
from . import views


app_name = 'monitor'
urlpatterns = [
    path('', views.index, name='index'),
    path('summary/', views.summary, name='summary'),
    path('refresh/', views.refresh, name='refresh')
]
