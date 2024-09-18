from django.urls import path,include
from user_api.views import *

urlpatterns = [
    
    path('user-registration', UserRegistration.as_view(), name='user-registration'),
    path('user-login', UserLogin.as_view(), name='user-login'),

    path('request-otp/', request_otp, name='request_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),

    
    path('category-with-subcategory-and-employees', category_with_subcategory_and_employees, name='category-with-subcategory-and-employees'),
    path('all-categories', all_categories, name='all-categories'), 
    
    path('user-profile-api', user_profile_api, name='user-profile-api'),
    path('edit-user-profile', edit_user_profile, name='edit-user-profile'),
    path('search-by-category', search_by_category, name='search-by-category'), 
    path('save-employee', save_employee, name='save-employee'),
    path('booking-api', booking_api, name='booking-api'),
    path('reschedule-booking', reschedule_booking, name='reschedule-booking'),

    path('my-orders-user-api', my_orders_user_api, name='my-orders-user-api'),
    path('post-review', post_review, name='post-review'),


]
