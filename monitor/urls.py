from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views


app_name = 'monitor'
urlpatterns = [
    path('', views.index, name='index'),
    path('summary/', views.summary, name='summary'),
    path('search/', views.search_dates, name='search'),
    path('refresh/', views.refresh, name='refresh'),
    path(
        'login/',
        auth_views.login,
        {'template_name': 'monitor/login.html'},
        name='login'
    ),
    path(
        'logout/',
        auth_views.logout,
        {'next_page': 'monitor:login'},
        name='logout'
    ),
]
