from rest_framework import serializers
from siyyana_app.models import *



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'



class StateSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    class Meta:
        model = State
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    class Meta:
        model = District
        fields = '__all__'




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'logo']


    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        return None 

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'service']




class RequestedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedCategory
        fields = ['id', 'name', 'subcategory']