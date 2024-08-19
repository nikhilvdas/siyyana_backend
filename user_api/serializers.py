from rest_framework import serializers
from accounts.models import *
from django.conf import settings
from siyyana_app.models import *



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['name', 'mobile_number', 'whatsapp_number', 'profile_picture']


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
        fields = ['id', 'name','count','subcategories']

    def get_subcategories(self, obj):
        subcategories = SubCategory.objects.filter(service=obj)
        return SubCategorySerializer(subcategories, many=True).data

    def get_count(self, obj):
        subcategories = SubCategory.objects.filter(service=obj).count()
        return subcategories
