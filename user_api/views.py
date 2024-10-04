from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from accounts.models import *
from rest_framework import status
from rest_framework.response import Response
from siyyana_app.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import random
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            country = request.data.get('country')
            state = request.data.get('state')
            district = request.data.get('district')
            fcm_token = request.data.get('fcm_token')
            mobile_number = request.data.get('mobile_number')
            whatsapp_number = request.data.get('whatsapp_number')
            country_instance = Country.objects.get(id=country)
            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=email, name=name, email=email, password=password,
                                                   fcm_token=fcm_token,country=country_instance, mobile_number=mobile_number,whatsapp_number=whatsapp_number,user_type="User")
            
            state_ids = request.data.get("state", "")
            state_ids = [int(id.strip()) for id in state_ids.split(",") if id.strip().isdigit()]

            if state_ids:
                state = []
                for i in state_ids:
                    statee = State.objects.get(id=i)
                    state.append(statee)
                user.state.set(state)

            district_ids = request.data.get("district", "")
            district_ids = [int(id.strip()) for id in district_ids.split(",") if id.strip().isdigit()]

            if district_ids:
                district = []
                for i in district_ids:
                    districtt = District.objects.get(id=i)
                    district.append(districtt)
                user.district.set(district)


            access_token = RefreshToken.for_user(user).access_token

            return Response({
                'message': 'User created successfully',
                'access_token': str(access_token),
                'refresh_token': str(RefreshToken.for_user(user).access_token),
                'user_details': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# class UserLogin(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if CustomUser.objects.filter(email=email).exists():
#             user = CustomUser.objects.get(email=email,user_type="User")
#             if user.check_password(password):
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'message': 'Login successful',
#                     'access_token': str(refresh.access_token),
#                     'refresh_token': str(refresh),
#                     'user_details': UserSerializer(user).data
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        fcm_token = request.data.get('fcm_token')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email, user_type="User").exists():
            user = CustomUser.objects.get(email=email, user_type="User")
            
            # Check password first
            if user.check_password(password):
                # Update FCM token only if it's provided
                if fcm_token:
                    user.fcm_token = fcm_token
                    user.save()

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_details': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)



def send_otp(email):
    return random.randint(1000, 9999)  # Generate a random 6-digit OTP

@csrf_exempt
def request_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = send_otp(email)
            request.session['email'] = email
            request.session['otp'] = otp
            user.otp = otp  # Save OTP in the user model
            user.otp_created_at = timezone.now()
            user.save()
            # Send OTP via email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {otp}.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'OTP sent successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User doesnot exist.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        print(type(otp))
        try:
            user = CustomUser.objects.get(email=email)
            if user.otp == otp:
                otp_age = timezone.now() - user.otp_created_at
                if otp_age <= timedelta(minutes=5):  # Check if OTP is still valid
                    return JsonResponse({'message': 'OTP verified successfully.','user_type':user.user_type})
                else:
                    return JsonResponse({'error': 'OTP has expired.'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid OTP.'}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Email not found.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            user = CustomUser.objects.get(email=email)
            print(user)
            print('user.otp',user.otp)
            print(otp)
            if str(user.otp) == str(otp):
                print('user.otp',user.otp)
                otp_age = timezone.now() - user.otp_created_at
                print('otp_age',otp_age)
                # if otp_age <= timedelta(minutes=5):
                print('====>')
                print('NEW PASSWORD',new_password)
                # Update the password and clear OTP
                user.set_password(new_password)
                user.otp = None  # Clear OTP after successful reset
                user.save()
                return JsonResponse({'message': 'Password reset successfully.'})
                # else:
                #     return JsonResponse({'error': 'OTP has expired.'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid OTP.'}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Email not found.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



from django.db.models.functions import Coalesce


@api_view(['GET','POST'])
def category_with_subcategory_and_employees(request):
    # Serialize all categories
    district = request.POST.get('district',None)
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request, 'district': district})

    # Fetch top categories with booking count annotation
    top_categories = Category.objects.annotate(
        booking_count=Count('subcategory__employyewages__service__employee')
    ).order_by('-booking_count')[:8]

    # Prepare the top categories data manually, as it's customized
    top_categories_data = []
    for category in top_categories:
        logo_url = request.build_absolute_uri(category.logo.url) if category.logo else None
        top_categories_data.append({
            'id': category.id,
            'name': category.name,
            'booking_count': category.booking_count,
            'logo': logo_url,
            'color': category.color,
        })

    # Handle top subcategories based on booking count
    top_subcategories = SubCategory.objects.annotate(
        booking_count=Count('employyewages__service__employee')  # Correcting the reference
    ).order_by('-booking_count')[:8]  # Fetching top 8 subcategories based on booking count

    top_subcategory_data = []
    for subcategory in top_subcategories:
        users = CustomUser.objects.filter(subcategory=subcategory).annotate(
            average_rating=Coalesce(Avg('employee_reviews__average_rating'), 0, output_field=FloatField())  # Explicitly set output_field to FloatField
        ).order_by('-average_rating')

        top_subcategory_data.append({
            'subcategory': {
                'id': subcategory.id,
                'category_id': subcategory.service.id if subcategory.service.id else None,
                'name': subcategory.name,
                'logo': request.build_absolute_uri(subcategory.logo.url) if subcategory.logo else None,
                'color': subcategory.color,
                'booking_count': subcategory.booking_count  # Include booking count here
            },
            'users': [{
                'id': user.id,
                'name': user.name,
                'mobile_number': user.mobile_number,
                'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
                'about': user.about,
                'charge': user.charge,
                'employee_wages': [{
                    'id': wage.id,
                    'subcategory': wage.subcategory.name,
                    'wages': wage.wages
                } for wage in EmployyeWages.objects.filter(user=user)],
                'ratings': {
                    'total_reviews': Review.objects.filter(employee=user).count(),
                    'average_rating': Review.objects.filter(employee=user).aggregate(Avg('average_rating')).get('average_rating', 0),
                    'timing_avg': Review.objects.filter(employee=user).aggregate(Avg('timing')).get('timing', 0),
                    'price_avg': Review.objects.filter(employee=user).aggregate(Avg('price')).get('price', 0),
                    'service_quality_avg': Review.objects.filter(employee=user).aggregate(Avg('service_quality')).get('service_quality', 0),
                    'behavior_avg': Review.objects.filter(employee=user).aggregate(Avg('behavior')).get('behavior', 0),
                }
            } for user in users]
        })

    # Return combined data
    return Response({
        'datas': serializer.data,
        'top_categories': top_categories_data,  # Manually prepared top categories
        'top_subcategories': top_subcategory_data  # Now includes top subcategories based on booking count
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
def booking_api(request):
    if request.method == 'POST':
        print(request.data)
        employee_id = request.data.get('employee_id')
        employee = CustomUser.objects.get(id=employee_id)
        service_id = request.data.get("service_id", "")
        booking_date = request.data.get('booking_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        service_id = [int(id.strip()) for id in service_id.split(",") if id.strip().isdigit()]
        print("===",service_id)
        # service = []
        for i in service_id:
            print("------",i)
            services = EmployyeWages.objects.get(id=i)
            Booking.objects.create(employee=employee, user=request.user, date=booking_date, start_time=start_time, end_time=end_time, service=services)
    return Response({'message': 'Booking created successfully'},status=status.HTTP_200_OK)




@api_view(['POST'])
def reschedule_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        # Retrieve the booking instance
        booking = get_object_or_404(Booking, id=booking_id)

        # Get the new date and time from the request data
        new_date = request.POST.get('date')
        new_start_time = request.POST.get('start_time')
        new_end_time = request.POST.get('end_time')

        # Update the booking instance with new values
        if new_date:
            booking.date = new_date
        if new_start_time:
            booking.start_time = new_start_time
        if new_end_time:
            booking.end_time = new_end_time
        
        # Save the updated booking instance
        booking.save()

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Booking rescheduled successfully'})
    
    # If the request method is not POST, return an error response
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)














# def all_categories(request):
#     categories_data = []

#     # Fetch all categories
#     categories = Category.objects.all()

#     for category in categories:
#         # Count subcategories/services under each category
#         service_count = SubCategory.objects.filter(service=category).count()
        
#         # Count employees related to the category
#         customuser_count = CustomUser.objects.filter(category=category).count()

#         # Append category data including service count and custom user count
#         categories_data.append({

#             'id': category.id,
#             'name': category.name,
#             'logo': request.build_absolute_uri(category.logo.url) if category.logo else None,
#             'subcategory_count': service_count,
#             'customuser_count': customuser_count,
            
#         })

#     # Return the data as a JSON response
#     return JsonResponse({'categories': categories_data}, safe=False)

def all_categories(request):
    categories_data = []

    # Fetch all categories
    categories = Category.objects.all()

    for category in categories:
        # Fetch subcategories under the current category
        subcategories = SubCategory.objects.filter(service=category)

        subcategory_count = subcategories.count()

        # Count employees (CustomUser) based on subcategory
        employees_in_subcategories = CustomUser.objects.filter(subcategory__in=subcategories).distinct()

        employee_count = employees_in_subcategories.count()

        categories_data.append({
            'id': category.id,
            'name': category.name,
            'logo': request.build_absolute_uri(category.logo.url) if category.logo else None,
            'subcategory_count': subcategory_count,
            'customuser_count': employee_count,
            'color': category.color,
            'subcategories': [{
                'id': sub.id,
                'name': sub.name,
                'logo': request.build_absolute_uri(sub.logo.url) if sub.logo else None,
                'employees': employees_in_subcategories.filter(subcategory=sub).count(),  # Employee count for each subcategory
            } for sub in subcategories]  # List all subcategories
        })

    # Return the data as a JSON response
    return JsonResponse({'categories': categories_data}, safe=False)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api(request):
    user = request.user

    # Serialize the foreign key fields
    country = user.country.name if user.country else None

    # CustomUser data
    user_data = {

        'id': user.id,
        'name': user.name,
        'mobile_number': user.mobile_number,
        'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
        'whatsapp_number': user.whatsapp_number,
        'email': user.email,
        'country': country,  # Serializing the country name
        'state': [
            {'id': state.id, 'name': state.name}
            for state in user.state.all()
        ],
        'district': [
            {'id': district.id, 'name': district.name}
            for district in user.district.all()
        ],
    }
    
    return JsonResponse(user_data)


@api_view(['POST'])
def search_by_category(request):
    category_name = request.data.get('category', None)
    district = request.data.get('district', None)
    if district:
            district = District.objects.get(name=district)
    else:
        district = None

    usr = None
    if not district:
        usr = request.user
        usr = CustomUser.objects.get(id=usr.id)
        district = usr.district.all()
    

    if not category_name:
        return JsonResponse({'error': 'Category name is required.'}, status=400)

    # try:
        # Get the category that matches the search term
    category = Category.objects.get(name__icontains=category_name)
    
    # Fetch users associated with the category
    if category:
        if not usr:
            users = CustomUser.objects.filter(category=category,district = district).distinct()
        else:
            users = CustomUser.objects.filter(category=category,district__in = district).distinct()

    user_data = []
    for user in users:
        # Fetch the employee's work schedule
        work_schedule = EmployeeWorkSchedule.objects.filter(user=user).first()
        work_schedule_data = {
            'sunday': f"{work_schedule.sunday_start_time} - {work_schedule.sunday_end_time}" if work_schedule else None,
            'monday': f"{work_schedule.monday_start_time} - {work_schedule.monday_end_time}" if work_schedule else None,
            'tuesday': f"{work_schedule.tuesday_start_time} - {work_schedule.tuesday_end_time}" if work_schedule else None,
            'wednesday': f"{work_schedule.wednesday_start_time} - {work_schedule.wednesday_end_time}" if work_schedule else None,
            'thursday': f"{work_schedule.thursday_start_time} - {work_schedule.thursday_end_time}" if work_schedule else None,
            'friday': f"{work_schedule.friday_start_time} - {work_schedule.friday_end_time}" if work_schedule else None,
            'saturday': f"{work_schedule.saturday_start_time} - {work_schedule.saturday_end_time}" if work_schedule else None,
        }

        # Fetch the employee's wages
        wages_list = []
        employee_wages = EmployyeWages.objects.filter(user=user)
        for wage in employee_wages:
            wages_list.append({
                "id": wage.id,
                "subcategory": wage.subcategory.name if wage.subcategory else None,
                "wages": wage.wages
            })

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

        # Construct user data including work schedule, wages, and review ratings
        user_data.append({
            'id': user.id,
            'name': user.name,
            'mobile_number': user.mobile_number,
            'whatsapp_number': user.whatsapp_number,
            'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
            'about': user.about,
            'work_schedule': work_schedule_data,  # Include the work schedule here
            'wages': wages_list,  # Include the wages here
            'ratings': rating_summary  # Include the review ratings here
        })

    # Response format includes the searched category and the list of users with work schedule and wages
    return JsonResponse({
        'searched_category': category.name,
        'users': user_data
    }, status=200)

    # except Category.DoesNotExist:
    #     return JsonResponse({'error': 'Category not found.'}, status=404)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def save_employee(request):
    user = request.user
    if request.method == 'GET':
        saved_employees = Saved_Employees.objects.filter(user=user)
        employees_list = []
        for saved in saved_employees:
            # Fetch the employee's work schedule
            work_schedule = EmployeeWorkSchedule.objects.filter(user=saved.employee).first()
            work_schedule_data = {
                'sunday': f"{work_schedule.sunday_start_time} - {work_schedule.sunday_end_time}" if work_schedule else None,
                'monday': f"{work_schedule.monday_start_time} - {work_schedule.monday_end_time}" if work_schedule else None,
                'tuesday': f"{work_schedule.tuesday_start_time} - {work_schedule.tuesday_end_time}" if work_schedule else None,
                'wednesday': f"{work_schedule.wednesday_start_time} - {work_schedule.wednesday_end_time}" if work_schedule else None,
                'thursday': f"{work_schedule.thursday_start_time} - {work_schedule.thursday_end_time}" if work_schedule else None,
                'friday': f"{work_schedule.friday_start_time} - {work_schedule.friday_end_time}" if work_schedule else None,
                'saturday': f"{work_schedule.saturday_start_time} - {work_schedule.saturday_end_time}" if work_schedule else None,
            }

            # Fetch the employee's wages
            wages_list = []
            employee_wages = EmployyeWages.objects.filter(user=saved.employee)
            for wage in employee_wages:
                wages_list.append({
                    "id": wage.id,
                    "subcategory": wage.subcategory.name if wage.subcategory else None,
                    "wages": wage.wages
                })

            # Fetch reviews for the employee
            reviews = Review.objects.filter(employee=saved.employee).order_by('-review_date')

            # Calculate overall rating and rating distribution
            rating_summary = {
                'total_reviews': reviews.count(),
                'average_rating': reviews.aggregate(average_rating=Avg('average_rating'))['average_rating'],
                'timing_avg': reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'],
                'price_avg': reviews.aggregate(price_avg=Avg('price'))['price_avg'],
                'service_quality_avg': reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'],
                'behavior_avg': reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'],
            }

            # Append employee data with ratings
            employees_list.append({

                "id": saved.employee.id,
                "employee_name": saved.employee.name,
                "employee_mobile": saved.employee.mobile_number,
                "employee_whatsapp": saved.employee.whatsapp_number,
                "employee_profile_picture": request.build_absolute_uri(saved.employee.profile_picture.url) if saved.employee.profile_picture else None,
                "employee_about": saved.employee.about,
                "work_schedule": work_schedule_data,  # Include work schedule in the response
                "wages": wages_list,  # Include wages list in the response
                "ratings": rating_summary  # Include review ratings in the response
                
            })


        return JsonResponse({"saved_employees": employees_list}, status=200)

    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return JsonResponse({"error": "Employee ID is required"}, status=400)

        employee = get_object_or_404(CustomUser, id=employee_id)

        saved_employee, created = Saved_Employees.objects.get_or_create(user=user, employee=employee)

        if created:
            return JsonResponse({"message": "Employee saved successfully"}, status=201)
        else:
            # Employee is already saved, so unsave (delete) it
            saved_employee.delete()
            return JsonResponse({"message": "Employee is unsaved successfully"}, status=200)

    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)



import calendar
from django.db.models import Q
@api_view(['POST'])
def my_orders_user_api(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    # Get the filter option from the POST data (not query parameters)
    date_filter = request.data.get('filter', 'All')

    # Define date ranges based on the filter option
    today = timezone.now().date()
    print(f"Filter selected: {date_filter}")
    
    if date_filter == 'Today':
        date_range = (today, today)
        print(f"Filtering for today: {date_range}")
    elif date_filter == 'This Week':
        start_date = today - timedelta(days=today.weekday())  # Start of the week
        end_date = start_date + timedelta(days=6)  # End of the week
        date_range = (start_date, end_date)
        print(f"Filtering for this week: {start_date} to {end_date}")
    elif date_filter == 'This Month':
        start_date = today.replace(day=1)  # Start of the month
        _, last_day_of_month = calendar.monthrange(today.year, today.month)  # Get last day of the month
        end_date = today.replace(day=last_day_of_month)  # End of the month
        date_range = (start_date, end_date)
        print(f"Filtering for this month: {start_date} to {end_date}")
    else:
        date_range = None
        print("No date range filtering applied")

    # Apply the filters using Q objects
    query = Q(user=request.user)
    
    if date_range:
        query &= Q(created_date__range=date_range)

    # Fetch and filter bookings based on each status for the logged-in user
    pending_bookings = Booking.objects.filter(query & Q(status='Pending')).order_by('-id')
    accepted_bookings = Booking.objects.filter(query & Q(status='Accept')).order_by('-id')
    completed_bookings = Booking.objects.filter(query & Q(status='Completed')).order_by('-id')
    rejected_bookings = Booking.objects.filter(query & Q(status='Reject')).order_by('-id')

    print(f"Pending bookings: {pending_bookings}")
    print(f"Accepted bookings: {accepted_bookings}")
    print(f"Completed bookings: {completed_bookings}")
    print(f"Rejected bookings: {rejected_bookings}")

    # Serialize the bookings using BookingSerializerUser
    pending_serializer = BookingSerializerUser(pending_bookings, many=True, context={'request': request})
    accepted_serializer = BookingSerializerUser(accepted_bookings, many=True, context={'request': request})
    completed_serializer = BookingSerializerUser(completed_bookings, many=True, context={'request': request})
    rejected_serializer = BookingSerializerUser(rejected_bookings, many=True, context={'request': request})

    # Return the data in a structured response
    return Response({
        'pending_bookings': pending_serializer.data,
        'accepted_bookings': accepted_serializer.data,
        'completed_bookings': completed_serializer.data,
        'rejected_bookings': rejected_serializer.data,
    })





@api_view(['POST'])
def post_review(request):
    try:
        # Load JSON data from request body
        data = request.data
        user = request.user
        # Extract fields from the request
        booking_id = data.get('booking_id')
        timing = data.get('timing')
        service_quality = data.get('service_quality')
        price = data.get('price')
        behavior = data.get('behavior')
        service_summary = data.get('service_summary', '')
        review_text = data.get('review', '')
        
        # Validate required fields
        if not all([booking_id, timing, service_quality, behavior]):
            return JsonResponse({'error': 'All required fields are missing'}, status=400)
        
        # Check if the booking exists
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Invalid booking ID'}, status=400)
        
        # Create the review
        review = Review.objects.create(
            booking=booking,
            employee=booking.employee,
            timing=timing,
            user = user,
            service_quality=service_quality,
            price=price,
            behavior=behavior,
            service_summary=service_summary,
            review=review_text
        )
        
        # Return success response
        return JsonResponse({'message': 'Review posted successfully'}, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_user_profile(request):
    user = request.user

    # Update the allowed CustomUser fields

    if request.POST.get('name') != '':
        user.name = request.POST.get('name', user.name)
    if request.POST.get('email') != '':
        user.email = request.POST.get('email', user.email)
    if request.POST.get('whatsapp_number') != '':
        user.whatsapp_number = request.POST.get('whatsapp_number', user.whatsapp_number)
    if request.POST.get('mobile_number') != '':
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
    if request.POST.get('country_id') != '':
        user.country_id = request.POST.get('country_id', user.country_id)
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']

    # Save the updated CustomUser model
    user.save()

    state_ids = request.data.get("state", "")
    state_ids = [int(id.strip()) for id in state_ids.split(",") if id.strip().isdigit()]

    if state_ids:
        state = []
        for i in state_ids:
            statee = State.objects.get(id=i)
            state.append(statee)
        user.state.set(state)

    district_ids = request.data.get("district", "")
    district_ids = [int(id.strip()) for id in district_ids.split(",") if id.strip().isdigit()]

    if district_ids:
        district = []
        for i in district_ids:
            districtt = District.objects.get(id=i)
            district.append(districtt)
        user.district.set(district)

    return JsonResponse({'status': 'success', 'message': 'User profile updated successfully'})









# Function-based view to get popular categories by booking count
def popular_categories(request):
    # Aggregate bookings count for each category and order by highest count
    categories = Category.objects.annotate(
        booking_count=Count('subcategory__employyewages__service__employee')
    ).order_by('-booking_count')[:5]

    # Prepare the response data
    # Prepare the response data
    result = []
    for category in categories:
        logo_url = request.build_absolute_uri(category.logo.url) if category.logo else None
        
        result.append({
            'id': category.id,
            'name': category.name,
            'booking_count': category.booking_count,
            'logo': logo_url,
            'color': category.color,
        })

    return JsonResponse(result, safe=False)