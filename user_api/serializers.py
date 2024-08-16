from rest_framework import serializers
from accounts.models import *
from django.conf import settings
from siyyana_app.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'