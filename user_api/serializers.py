from rest_framework import serializers
from accounts.models import *
from django.conf import settings
from siyyana_app.models import *
from employee_api.serializers import *
from django.db.models import Count


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
        logged_in_user = self.context['request'].user
        district = self.context.get('district')
        if district:
            district = District.objects.get(name=district)
        else:
            district = None
        
        if not district:
            district = logged_in_user.district.all()
            users = CustomUser.objects.filter(subcategory=obj, user_type="Employee",district__in=district).annotate(
            # Annotate the users with the average rating, replacing null with 0
            average_rating=Coalesce(Avg('employee_reviews__average_rating'), 0, output_field=FloatField())
        ).order_by(
            # Sort by average_rating, but put users with 0 rating at the bottom
            '-average_rating', 'id'
        ).distinct()
        else:
            users = CustomUser.objects.filter(subcategory=obj, user_type="Employee",district=district).annotate(
            # Annotate the users with the average rating, replacing null with 0
            average_rating=Coalesce(Avg('employee_reviews__average_rating'), 0, output_field=FloatField())
        ).order_by(
            # Sort by average_rating, but put users with 0 rating at the bottom
            '-average_rating', 'id'
        ).distinct()
        user_data = []
        # Get the current logged-in user from the context

        for user in users:
            # Serialize the user data
            user_info = UserSerializer(user).data

            # Fetch reviews for the employee
            reviews = Review.objects.filter(employee=user)

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
    
from django.db.models.functions import Coalesce
from django.db.models import Avg, FloatField


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    all_employees = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'logo', 'color', 'count', 'all_employees', 'subcategories']

    def get_subcategories(self, obj):
        request = self.context.get('request')
        district = self.context.get('district')
        subcategories = SubCategory.objects.filter(service=obj)
        subcategory_data = SubCategorySerializer(subcategories, many=True, context={'request': request, 'district': district}).data

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
        district = self.context.get('district')
        if district:
            district = District.objects.get(name=district)
        else:
            district = None

        # Get subcategories related to the current category
        subcategories = SubCategory.objects.filter(service=obj)
        employee_count = 0  # Initialize employee count
        all_employee_list = []
        usr = None
        if not district:
            usr = request.user
            usr = CustomUser.objects.get(id=usr.id)
            district = usr.district.all()
            print(district)

        # Check if there are subcategories
        # If there are subcategories, fetch employees
        if subcategories.exists():
            if not usr:
                users = CustomUser.objects.filter(subcategory__in=subcategories, user_type="Employee", district=district).annotate(
                    average_rating=Coalesce(Avg('employee_reviews__average_rating'), 0, output_field=FloatField())  # Set output_field to FloatField
                ).order_by('-average_rating').distinct()
            else:
                users = CustomUser.objects.filter(subcategory__in=subcategories, user_type="Employee", district__in=district).annotate(
                    average_rating=Coalesce(Avg('employee_reviews__average_rating'), 0, output_field=FloatField())  # Set output_field to FloatField
                ).order_by('-average_rating').distinct()

            for user in users:
                # Fetch reviews for the employee
                reviews = Review.objects.filter(employee=user)

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
                    'phone' : user.mobile_number,
                    'whatsapp': user.whatsapp_number,
                    'ratings': rating_summary,
                    'employee_wages': wages_data  # Include wages data here
                }

                all_employee_list.append(employee_info)

            # Update employee count based on users found
            employee_count = users.count()

        # If no subcategories, return empty list
        else:
            all_employee_list = []

        return {
            'employee_count': employee_count,  # Return the employee count
            'all': all_employee_list  # List of employees or empty
        }

class TopCategorySerializer(serializers.ModelSerializer):
    Category = CategoryListSerializer(read_only=True)

    class Meta:
        model = TopCategory
        fields = ['id', 'Category']

    def to_representation(self, instance):
        # Annotate the categories with booking_count
        categories = Category.objects.annotate(
            booking_count=Count('subcategory__employyewages__service__employee')
        ).order_by('-booking_count')[:5]

        # Prepare the response data
        result = []  # This will store category details
        request = self.context.get('request')  # To access request for absolute URI
        for category in categories:
            # Build the logo URL
            logo_url = request.build_absolute_uri(category.logo.url) if category.logo else None
            
            # Append category data directly to result
            result.append({
                'id': category.id,
                'name': category.name,
                'booking_count': category.booking_count,
                'logo': logo_url,
                'color': category.color,
            })

        # Directly return the result list, ensuring no extra list wrapping
        return result
    


    
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
        # if obj.status == 'Completed':
        reviews = obj.reviews.all()
        return ReviewSerializerUser(reviews, many=True).data
        # return None






