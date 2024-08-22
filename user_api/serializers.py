from rest_framework import serializers
from accounts.models import *
from django.conf import settings
from siyyana_app.models import *
from employee_api.serializers import *


class UserSerializer(serializers.ModelSerializer):
    employee_wages = EmplpoyeeWagesSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id','name','email', 'mobile_number', 'whatsapp_number', 'profile_picture','employee_wages','charge']


class SubCategorySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'users']

    def get_users(self, obj):
        # Filtering users associated with this particular subcategory
        users = CustomUser.objects.filter(subcategory=obj,user_type="Employee")
        return UserSerializer(users, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name','logo','count','subcategories']

    def get_subcategories(self, obj):
        subcategories = SubCategory.objects.filter(service=obj)
        return SubCategorySerializer(subcategories, many=True).data

    def get_count(self, obj):
        subcategories = SubCategory.objects.filter(service=obj).count()
        return subcategories

















