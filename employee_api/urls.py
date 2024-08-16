from django.urls import path,include
from employee_api import views

urlpatterns = [
    
    path('location-list-api', views.location_list_api,name='location-list-api'),
]
