from django.urls import path,include
from user_api.views import *

urlpatterns = [
    
    path('user-registration', UserRegistration.as_view(), name='user-registration'),
    path('user-login', UserLogin.as_view(), name='user-login'),
    path('category-with-subcategory-and-employees', category_with_subcategory_and_employees, name='category-with-subcategory-and-employees'),
    path('all-categories', all_categories, name='all-categories'), 
    path('user-profile-api', user_profile_api, name='user-profile-api'), 
    path('search-by-category', search_by_category, name='search-by-category'), 

    path('save-employee', save_employee, name='save-employee'),

    path('booking-api', booking_api, name='booking-api'),

]
