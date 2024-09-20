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
        # Filtering users associated with this particular subcategory
        users = CustomUser.objects.filter(subcategory=obj,user_type="Employee")
        return UserSerializer(users, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    all_employees= serializers.SerializerMethodField()


    class Meta:
        model = Category
        fields = ['id', 'name','logo','color','count','all_employees','subcategories']

    def get_subcategories(self, obj):
        subcategories = SubCategory.objects.filter(service=obj)
        return SubCategorySerializer(subcategories, many=True).data

    def get_count(self, obj):
        subcategories = SubCategory.objects.filter(service=obj).count()
        return subcategories
    
    def get_all_employees(self, obj):
        request = self.context.get('request')
        users = CustomUser.objects.filter(category=obj, user_type="Employee")

        employee_data = []
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

            # rating_distribution = {
            #     '5_star': reviews.filter(average_rating__gte=4.9).count(),
            #     '4_star': reviews.filter(average_rating__gte=3.9, average_rating__lt=4.9).count(),
            #     '3_star': reviews.filter(average_rating__gte=2.9, average_rating__lt=3.9).count(),
            #     '2_star': reviews.filter(average_rating__gte=1.9, average_rating__lt=2.9).count(),
            #     '1_star': reviews.filter(average_rating__lt=1.9).count(),
            # }

            # Manually create a list of review data for each review
            # reviews_list = [
            #     {
            #         'user_name': review.user.name if review.user else "Anonymous",
            #         'profile_pic': request.build_absolute_uri(review.user.profile_picture.url) if review.user and review.user.profile_picture else None,
            #         'review_date': review.review_date.strftime("%b %Y"),
            #         'average_rating': review.average_rating,
            #         'service_summary': review.service_summary,
            #         'review': review.review,
            #     }
            #     for review in reviews
            # ]

            # Add employee data along with rating and review information
            employee_data.append({
                'employee_id': user.id,
                'name': user.name,
                'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
                'rating_summary': rating_summary,
                # 'rating_distribution': rating_distribution,
                # 'reviews': reviews_list
            })
        
        return employee_data



class TopCategorySerializer(serializers.ModelSerializer):
    Category = CategoryListSerializer(read_only=True)

    class Meta:
        model = TopCategory
        fields = ['id', 'Category']




class BookingSerializerUser(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    service = EmplpoyeeWagesSerializer() 
    class Meta:
        model = Booking
        fields = ['id', 'employee', 'service', 'date', 'start_time', 'end_time', 'status']






