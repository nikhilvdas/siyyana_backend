from django.urls import path,include
from user_api import views

urlpatterns = [
    
    path('', views.index,name='index'),
]
