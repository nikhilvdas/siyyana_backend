from django.urls import path,include
from employee_api import views
from employee_api.views import *


urlpatterns = [
    
    path('location-list-api', views.location_list_api,name='location-list-api'),
    path('employee-registration', EmployeeRegistration.as_view(), name='employee-registration'),
    path('employee-login', EmployeeLogin.as_view(), name='employee-login'),

    path('category-list', views.category_list, name='category-list'),
    path('subcategories-by-category', views.subcategories_by_category, name='subcategories-by-category'),
    path('requested-category-api', views.requested_category_api, name='requested-category-api'),

]
