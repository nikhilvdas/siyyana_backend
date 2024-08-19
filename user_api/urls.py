from django.urls import path,include
from user_api.views import *

urlpatterns = [
    
    path('user-registration', UserRegistration.as_view(), name='user-registration'),
    path('user-login', UserLogin.as_view(), name='user-login'),
    path('category-with-subcategory-and-employees', category_with_subcategory_and_employees, name='category-with-subcategory-and-employees'),
    
]
