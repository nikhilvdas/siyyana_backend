from rest_framework import serializers
from siyyana_app.models import *



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'