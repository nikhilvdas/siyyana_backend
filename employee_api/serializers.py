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