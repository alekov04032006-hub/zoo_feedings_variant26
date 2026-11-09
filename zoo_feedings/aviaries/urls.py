from django.urls import path
from . import views
app_name = 'aviaries'
urlpatterns = [path('', views.aviary_list, name='list')]
