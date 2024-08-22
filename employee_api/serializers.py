from rest_framework import serializers
from accounts.models import CustomUser, EmployyeWages
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



class EmplpoyeeWagesSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()
    class Meta:
        model = EmployyeWages
        fields = ['id','subcategory','wages']



class EmployeeSerializer(serializers.ModelSerializer):
    employee_wages = EmplpoyeeWagesSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','profile_picture','about','employee_wages','charge']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None 



# class BookingSerializer(serializers.ModelSerializer):
#     service = EmplpoyeeWagesSerializer(many=True)
#     employee = serializers.StringRelatedField()
#     user = serializers.StringRelatedField()
#     class Meta:
#         model = Booking
#         fields = '__all__'


class UserSerializerForBookingDetails(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name','email', 'mobile_number', 'whatsapp_number', 'profile_picture']



class BookingSerializer(serializers.ModelSerializer):
    category_logo = serializers.SerializerMethodField()
    service = EmplpoyeeWagesSerializer(many=True)
    employee = serializers.StringRelatedField()
    user = UserSerializerForBookingDetails()

    class Meta:
        model = Booking
        fields = ["id",'employee', 'date', 'status', 'category_logo','service','user']

    def get_category_logo(self, obj):
        # Assuming you're only fetching the first related category logo.
        if obj.service.exists():
            employye_wage = obj.service.first()
            if employye_wage.subcategory and employye_wage.subcategory.service:
                return employye_wage.subcategory.service.logo.url
        return None