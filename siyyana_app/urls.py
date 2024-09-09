from django.urls import path,include
from siyyana_app import views

app_name = 'siyyana_app'
urlpatterns = [
    
    
    path('', views.login,name='login'),
    path('admin-logout', views.admin_logout,name='admin_logout'),
    
    path('dashboard', views.index,name='index'),
    path('services', views.services,name='services'),
    path('add-services', views.add_services,name='add_services'),
    path('edit-services/<int:id>/', views.edit_services,name='edit_services'),
    path('delete-services/<int:id>/', views.delete_services,name='delete_services'),


    path('sub-services', views.sub_services,name='sub_services'),
    path('add-subservices', views.add_subservices,name='add_subservices'),
    path('edit-subservices/<int:id>/', views.edit_subservices,name='edit_subservices'),
    path('delete-subservices/<int:id>/', views.delete_subservices,name='delete_subservices'),

    path('top-services', views.top_services,name='top_services'),
    path('add-topservices', views.add_topservices,name='add_topservices'),
    path('edit-topservices/<int:id>/', views.edit_topservices,name='edit_topservices'),
    path('delete-topservices/<int:id>/', views.delete_topservices,name='delete_topservices'),

    path('employee-list', views.employee_list,name='employee_list'),
    path('employee-delete/<int:id>/', views.employee_delete,name='employee_delete'),
    

    path('user-list', views.user_list,name='user_list'),
    path('user-delete/<int:id>/', views.user_delete,name='user_delete'),

    
]
