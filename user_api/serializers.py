from rest_framework import serializers
from accounts.models import *
from django.conf import settings
from siyyana_app.models import *
from employee_api.serializers import *



class UserSerializer(serializers.ModelSerializer):
    employee_wages = EmplpoyeeWagesSerializer(many=True)
    employee_work_schedule = EmployeeWorkScheduleSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id','name','email', 'mobile_number', 'whatsapp_number', 'profile_picture','employee_wages','charge','employee_work_schedule']


class SubCategorySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'users']

    def get_users(self, obj):
        users = CustomUser.objects.filter(subcategory=obj, user_type="Employee")
        user_data = []

        for user in users:
            # Serialize the user data
            user_info = UserSerializer(user).data

            # Fetch reviews for the employee
            reviews = Review.objects.filter(employee=user).order_by('-review_date')

            # Calculate overall rating and rating distribution
            rating_summary = {
                'total_reviews': reviews.count(),
                'average_rating': reviews.aggregate(average_rating=Avg('average_rating'))['average_rating'],
                'timing_avg': reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'],
                'price_avg': reviews.aggregate(price_avg=Avg('price'))['price_avg'],
                'service_quality_avg': reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'],
                'behavior_avg': reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'],
            }

            # Add the calculated ratings outside of employee_work_schedule
            user_info['ratings'] = rating_summary

            # Append the modified user data
            user_data.append(user_info)

        return user_data
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    all_employees = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'logo', 'color', 'count', 'all_employees', 'subcategories']

    def get_subcategories(self, obj):
        subcategories = SubCategory.objects.filter(service=obj)
        subcategory_data = SubCategorySerializer(subcategories, many=True).data

        # Create the "All employees" subcategory
        all_employees_data = self.get_all_employees(obj)
        all_employees_subcategory = {
            'id': None,  # You can assign a special ID or leave it as None
            'name': 'All employees',
            'users': all_employees_data['all']
        }

        # Prepend the "All employees" subcategory to the response
        return [all_employees_subcategory] + subcategory_data

    def get_count(self, obj):
        subcategories = SubCategory.objects.filter(service=obj).count()
        return subcategories

    def get_all_employees(self, obj):
        request = self.context.get('request')
        users = CustomUser.objects.filter(category=obj, user_type="Employee")

        all_employee_list = []

        for user in users:
            # Fetch reviews for the employee
            reviews = Review.objects.filter(employee=user).order_by('-review_date')

            # Calculate overall rating and rating distribution
            rating_summary = {
                'total_reviews': reviews.count(),
                'average_rating': reviews.aggregate(average_rating=Avg('average_rating'))['average_rating'],
                'timing_avg': reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'],
                'price_avg': reviews.aggregate(price_avg=Avg('price'))['price_avg'],
                'service_quality_avg': reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'],
                'behavior_avg': reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'],
            }

            # Fetch employee wages for each subcategory
            employee_wages = EmployyeWages.objects.filter(user=user)
            wages_data = [{
                'id': wage.id,
                'subcategory': wage.subcategory.name if wage.subcategory else None,
                'wages': wage.wages
            } for wage in employee_wages]

            # Build individual employee data with wages
            employee_info = {
                'id': user.id,
                'name': user.name,
                'profile_picture': user.profile_picture.url,
                'rating_summary': rating_summary,
                'employee_wages': wages_data  # Include wages data here
            }

            all_employee_list.append(employee_info)

        return {
            'all': all_employee_list
        }


class TopCategorySerializer(serializers.ModelSerializer):
    Category = CategoryListSerializer(read_only=True)

    class Meta:
        model = TopCategory
        fields = ['id', 'Category']



class ReviewSerializerUser(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['timing', 'service_quality', 'price', 'behavior', 'service_summary', 'review', 'review_date', 'average_rating']



class BookingSerializerUser(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    service = EmplpoyeeWagesSerializer()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'employee', 'service', 'date', 'start_time', 'end_time', 'status', 'reviews']

    def get_reviews(self, obj):
        if obj.status == 'Completed':
            reviews = obj.reviews.all()
            return ReviewSerializerUser(reviews, many=True).data
        return None






