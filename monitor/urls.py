from django.urls import path
from django.conf import settings
from . import views


app_name = 'monitor'
urlpatterns = [
    path('', views.index, name='index'),
    # path('prod/csv/', views.generate_csv, name='generate_csv'),
    # path('prod/')
]
