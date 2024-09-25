from django.urls import path,include
from employee_api import views
from employee_api.views import *


urlpatterns = [
    
    path('location-list-api', views.location_list_api,name='location-list-api'),
    path('state-list-api', views.state_list_api,name='state-list-api'),
    path('employee-registration', EmployeeRegistration.as_view(), name='employee-registration'),
    path('employee-login', EmployeeLogin.as_view(), name='employee-login'),
    path('employee-detail-api', employee_detail_api, name='employee-detail-api'),
    path('get-time-slots', get_time_slots, name='get-time-slots'),
    

    path('category-list', views.category_list, name='category-list'),
    path('subcategories-by-category', views.subcategories_by_category, name='subcategories-by-category'),
    path('requested-category-api', views.requested_category_api, name='requested-category-api'),
    

    path('employee-home', views.employee_home, name='employee-home'),
    path('employee-profile-api', views.employee_profile_api, name='employee-profile-api'),
    path('edit-employee-profile', views.edit_employee_profile, name='edit-employee-profile'),


    path('my-orders', views.my_orders, name='my-orders'),

    path('employee-all-reviews', views.employee_all_reviews, name='employee_all_reviews'),

    path('onboardings', views.get_onboardings, name='get_onboardings'),

    path('notification-history-api', views.notification_history_api, name='notification_history_api'),
    path('get-currency-types', views.get_currency_types, name='get_currency_types'),

    

]
