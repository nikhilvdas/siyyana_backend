from django.urls import path,include
from siyyana_app import views

urlpatterns = [
    
    path('', views.index,name='index'),
]
