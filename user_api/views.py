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
            state_instance = State.objects.get(id=state)
            district_instance = District.objects.get(id=district)
            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=email, name=name, email=email, password=password,
                                                   fcm_token=fcm_token,country=country_instance,state=state_instance,district=district_instance, mobile_number=mobile_number,whatsapp_number=whatsapp_number,user_type="User")
            access_token = RefreshToken.for_user(user).access_token

            return Response({
                'message': 'User created successfully',
                'access_token': str(access_token),
                'refresh_token': str(RefreshToken.for_user(user).access_token),
                'user_details': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email,user_type="User")
            if user.check_password(password):
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
            return JsonResponse({'error': 'Email not found.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user = CustomUser.objects.get(email=request.session['email'])
            if user.otp == otp:
                otp_age = timezone.now() - user.otp_created_at
                if otp_age <= timedelta(minutes=5):  # Check if OTP is still valid
                    return JsonResponse({'message': 'OTP verified successfully.'})
                else:
                    return JsonResponse({'error': 'OTP has expired.'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid OTP.'}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Email not found.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
def reset_password(request):
    print(request.session['otp'])
    if request.method == 'POST':
        otp = request.session['otp']
        print(otp)
        new_password = request.POST.get('new_password')

        try:
            user = CustomUser.objects.get(email=request.session['email'])
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





@api_view(['GET'])
def category_with_subcategory_and_employees(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    top_categories = TopCategory.objects.all()
    topcategories_serializer = TopCategorySerializer(top_categories, many=True, context={'request': request})
    return Response({'datas': serializer.data,'top_categories': topcategories_serializer.data}, status=status.HTTP_200_OK)





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















def all_categories(request):
    categories_data = []

    categories = Category.objects.all()
    for category in categories:
        subcategory_count = category.subcategory_set.count()
        customuser_count = CustomUser.objects.filter(category=category).count()

        categories_data.append({
            'id': category.id,
            'name': category.name,
            'logo': request.build_absolute_uri(category.logo.url) if category.logo else None,
            'subcategory_count': subcategory_count,
            'customuser_count': customuser_count,
        })

    return JsonResponse({'categories': categories_data}, safe=False)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api(request):
    user = request.user
    # CustomUser data
    user_data = {
        'id': user.id,
        'name': user.name,
        'mobile_number': user.mobile_number,
        'whatsapp_number': user.whatsapp_number,
        'email': user.email,
    }
    

    return JsonResponse(user_data)



@api_view(['POST'])
def search_by_category(request):
    category_name = request.data.get('category', None)
    if not category_name:
        return JsonResponse({'error': 'Category name is required.'}, status=400)

    try:
        # Get the category that matches the search term
        category = Category.objects.get(name__icontains=category_name)
        
        # Fetch users associated with the category
        users = CustomUser.objects.filter(category=category).distinct()

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

            user_data.append({
                'name': user.name,
                'mobile_number': user.mobile_number,
                'whatsapp_number': user.whatsapp_number,
                'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
                'about': user.about,
                'work_schedule': work_schedule_data,  # Include the work schedule here
            })

        # Response format includes the searched category and the list of users with work schedule
        return JsonResponse({
            'searched_category': category.name,
            'users': user_data
        }, status=200)

    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found.'}, status=404)    


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

            employees_list.append({
                "id": saved.employee.id,
                "employee_name": saved.employee.name,
                "employee_mobile": saved.employee.mobile_number,
                "employee_whatsapp": saved.employee.whatsapp_number,
                "employee_profile_picture": request.build_absolute_uri(saved.employee.profile_picture.url) if saved.employee.profile_picture else None,
                "employee_about": saved.employee.about,
                "work_schedule": work_schedule_data  # Include work schedule in the response
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

@api_view(['GET'])
def my_orders_user_api(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    # Get the filter option from query parameters
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
        query &= Q(date__range=date_range)
    
    # Fetch and filter bookings based on each status for the logged-in user
    pending_bookings = Booking.objects.filter(query & Q(status='Pending'))
    accepted_bookings = Booking.objects.filter(query & Q(status='Accept'))
    completed_bookings = Booking.objects.filter(query & Q(status='Completed'))
    rejected_bookings = Booking.objects.filter(query & Q(status='Reject'))

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