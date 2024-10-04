from rest_framework import serializers
from accounts.models import CustomUser, EmployeeWorkSchedule, EmployeeWorkTimeSlot, EmployyeWages
from siyyana_app.models import *
from django.db.models import Avg



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'



class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    class Meta:
        model = State
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    class Meta:
        model = District
        fields = '__all__'




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'logo','color']


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


class ReviewSerializer(serializers.ModelSerializer):
    user_profile_picture = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['user', 'user_profile_picture', 'review_date', 'average_rating', 'service_summary', 'review']

    def get_user_profile_picture(self, obj):
        request = self.context.get('request')
        if request and obj.user and obj.user.profile_picture:
            return request.build_absolute_uri(obj.user.profile_picture.url)
        return None


# class EmployeeSerializer(serializers.ModelSerializer):
#     employee_wages = EmplpoyeeWagesSerializer(many=True)
#     total_orders = serializers.SerializerMethodField()
#     employee_work_schedule = EmployeeWorkScheduleSerializer(many=True)
#     reviews = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         # fields = ['id','first_name','last_name','profile_picture','mobile_number','whatsapp_number','about','total_orders','employee_wages','charge','employee_work_schedule_new']
#         fields = "__all__"

#     def get_logo(self, obj):
#         request = self.context.get('request')
#         if obj.profile_picture:
#             return request.build_absolute_uri(obj.profile_picture.url)
#         return None 

#     def get_total_orders(self, obj):
#         return Booking.objects.filter(employee=obj).count()
    
    
#     def get_reviews(self, obj):
#         # Get all reviews related to the employee
#         reviews = Review.objects.filter(employee=obj)
#         serialized_reviews = ReviewSerializer(reviews, many=True).data
#         # Calculate the average of average_rating field for all reviews of the employee
#         average_rating = Review.objects.filter(employee=obj).aggregate(Avg('average_rating'))['average_rating__avg']
#         # If there are no reviews, return 0 as the average rating
#         average_rating = round(average_rating, 1) if average_rating else 0
#         # Return a dictionary with overall average rating, count, and the reviews
#         return {
#             "overall_average_rating": average_rating,
#             "overall_rating_count": reviews.count(),
#             "review_list": serialized_reviews
#         }
    
#     def get_overall_rating_count(self, obj):
#         # Return the count of reviews related to the employee
#         return Review.objects.filter(employee=obj).count()




class EmployeeSerializer(serializers.ModelSerializer):
    employee_wages = EmplpoyeeWagesSerializer(many=True)
    total_orders = serializers.SerializerMethodField()
    employee_work_schedule = EmployeeWorkScheduleSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = "__all__"

    def get_logo(self, obj):
        request = self.context.get('request')
        if request and obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None

    def get_total_orders(self, obj):
        return Booking.objects.filter(employee=obj,status='Completed').count()

    def get_reviews(self, obj):
        reviews = Review.objects.filter(employee=obj)
        serialized_reviews = ReviewSerializer(reviews, many=True, context=self.context).data
        average_rating = Review.objects.filter(employee=obj).aggregate(Avg('average_rating'))['average_rating__avg']
        average_rating = round(average_rating, 1) if average_rating else 0
        return {
            "overall_average_rating": average_rating,
            "overall_rating_count": reviews.count(),
            "review_list": serialized_reviews
        }

    def get_overall_rating_count(self, obj):
        return Review.objects.filter(employee=obj).count()








class UserSerializerForBookingDetails(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['id','name','email', 'mobile_number', 'whatsapp_number', 'profile_picture']
        fields = "__all__"



class BookingSerializer(serializers.ModelSerializer):
    category_logo = serializers.SerializerMethodField()
    service = EmplpoyeeWagesSerializer()  # Remove `many=True`
    employee = serializers.StringRelatedField()
    user = UserSerializerForBookingDetails()
    employee_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ["id", 'employee','employee_reviews', 'date','start_time', 'end_time', 'status', 'category_logo', 'service', 'user']

    def get_category_logo(self, obj):
        request = self.context.get('request')
        if obj.service and obj.service.subcategory and obj.service.subcategory.service:
            logo_url = obj.service.subcategory.service.logo.url
            return request.build_absolute_uri(logo_url) if request else logo_url
        return None
    

    def get_employee_reviews(self, obj):
        # Retrieve reviews related to this specific booking
        reviews = Review.objects.filter(booking=obj)

        # Calculate review statistics
        rating_summary = {
            'total_reviews': reviews.count(),
            'average_rating': reviews.aggregate(average_rating=Avg('average_rating'))['average_rating'],
            'timing_avg': reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'],
            'price_avg': reviews.aggregate(price_avg=Avg('price'))['price_avg'],
            'service_quality_avg': reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'],
            'behavior_avg': reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'],
        }

        # If the booking status is 'Completed', include individual reviews
        if obj.status == 'Completed':
            individual_reviews = []
            for review in reviews:
                individual_reviews.append({
                    'id': review.id,
                    'user_id': review.user.id if review.user else None,
                    'timing': review.timing,
                    'service_quality': review.service_quality,
                    'price': review.price,
                    'behavior': review.behavior,
                    'service_summary': review.service_summary,
                    'review': review.review,
                    'review_date': review.review_date,
                    'average_rating': review.average_rating,
                })

            return {
                'rating_summary': rating_summary,
                'ratings': individual_reviews,  # Include the detailed reviews
            }
        
        return {
            'rating_summary': rating_summary,
            'ratings': [],  # Return an empty list if no reviews are present
        }



class EmployeeWorkTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeWorkTimeSlot
        fields = ['day', 'start_time', 'end_time']






class OnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onbaording
        fields = ['id', 'name', 'description', 'logo']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo:
            return request.build_absolute_uri(obj.logo.url)
        return None 