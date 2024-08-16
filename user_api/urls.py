from django.urls import path,include
from user_api.views import *

urlpatterns = [
    
    path('user-registration', UserRegistration.as_view(), name='user-registration'),
    path('user-login', UserLogin.as_view(), name='user-login'),

]
