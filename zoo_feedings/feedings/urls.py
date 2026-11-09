from django.urls import path
from . import views
app_name = 'feedings'
urlpatterns = [path('', views.feeding_list, name='list'),
               path('statistics/', views.statistics, name='statistics'),
               path('<slug:slug>/', views.feeding_detail, name='detail')]
