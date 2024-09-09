from rest_framework import serializers
from accounts.models import CustomUser, EmployeeWorkSchedule, EmployyeWages
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

class TopCategorySerializer(serializers.ModelSerializer):
    Category = CategoryListSerializer(read_only=True)

    class Meta:
        model = TopCategory
        fields = ['id', 'Category']


class RequestedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedCategory
        fields = ['id', 'name', 'subcategory']



class EmplpoyeeWagesSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()
    class Meta:
        model = EmployyeWages
        fields = ['id','subcategory','wages']


class EmployeeWorkScheduleSerializer(serializers.ModelSerializer):
    subcategory = serializers.StringRelatedField()
    class Meta:
        model = EmployeeWorkSchedule
        exclude = ['user']




class EmployeeSerializer(serializers.ModelSerializer):
    employee_wages = EmplpoyeeWagesSerializer(many=True)
    total_orders = serializers.SerializerMethodField()
    employee_work_schedule = EmployeeWorkScheduleSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','profile_picture','mobile_number','whatsapp_number','about','total_orders','employee_wages','charge','employee_work_schedule']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None 

    def get_total_orders(self, obj):
        return Booking.objects.filter(employee=obj).count()


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
    service = EmplpoyeeWagesSerializer()  # Remove `many=True`
    employee = serializers.StringRelatedField()
    user = UserSerializerForBookingDetails()

    class Meta:
        model = Booking
        fields = ["id", 'employee', 'date','start_time', 'end_time', 'status', 'category_logo', 'service', 'user']

    def get_category_logo(self, obj):
        request = self.context.get('request')
        if obj.service and obj.service.subcategory and obj.service.subcategory.service:
            logo_url = obj.service.subcategory.service.logo.url
            return request.build_absolute_uri(logo_url) if request else logo_url
        return None