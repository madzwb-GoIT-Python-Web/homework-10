from django.urls import path
from . import views

app_name = 'apps.quotes'

urlpatterns = [
    path('', views.main, name='main'),
]
