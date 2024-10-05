from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from siyyana_app.models import Country
from employee_api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import *
from siyyana_app.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from user_api.serializers import *
import json
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from datetime import timedelta
import re
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'user_api/index.html')



@api_view(['GET','POST'])
def location_list_api(request):
    if request.method == 'GET':
        locations = Country.objects.all()
        serializer = CountrySerializer(locations, many=True,context={'request':request})
        return Response(serializer.data)
    if request.method == 'POST':
        country_id = request.data.get('country_id')
        if country_id:
            country = Country.objects.get(id=country_id)
            state = State.objects.filter(country=country)
            serializer = StateSerializer(state, many=True,context={'request':request})
            return Response(serializer.data)
        
        state_ids = request.data.get("state_id", "")
        state_ids = [int(id.strip()) for id in state_ids.split(",") if id.strip().isdigit()]
        if state_ids:
            all_districts = []
            for i in state_ids:
                state = State.objects.get(id=i)  # Ensure the state exists
                districts = District.objects.filter(state=state)
                all_districts.extend(districts)  # Collect all districts

            # Serialize all districts together
            serializer = DistrictSerializer(all_districts, many=True, context={'request': request})
            return Response(serializer.data)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET'])
def state_list_api(request):
    states = State.objects.all()
    
    state_data = []
    for state in states:
        state_data.append({
            'id': state.id,
            'name': state.name,
        })
    
    return Response({'states': state_data}, status=200)

from datetime import datetime, timedelta, date
# Setup logging

def create_time_slots(user, day, start_time, end_time):
    """Utility function to create 1-hour time slots."""
    
    # Convert string inputs into time objects if necessary
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%H:%M').time()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, '%H:%M').time()
    
    # Delete existing slots for the user and day
    existing_slots = EmployeeWorkTimeSlot.objects.filter(user=user, day=day)
    
    if existing_slots.exists():
        existing_slots.delete()
        print(f"Deleted existing time slots for {day}")
    
    print('Entered create_time_slots function')
    
    # Set the initial time to start_time
    current_time = start_time

    while current_time < end_time:
        # Calculate the next time slot by adding 1 hour
        next_time = (datetime.combine(date.today(), current_time) + timedelta(hours=1)).time()

        # Ensure the next time does not exceed the end time
        if next_time > end_time:
            next_time = end_time

        # Create the time slot for this interval
        EmployeeWorkTimeSlot.objects.create(
            user=user,
            day=day,
            start_time=current_time,
            end_time=next_time
        )
        print(f"Created time slot from {current_time} to {next_time}")
        
        # Move to the next time slot
        current_time = next_time
        
        # Break if the next time equals the end time
        if current_time == end_time:
            break

    print('Time slots created successfully')


class EmployeeRegistration(APIView):
    
    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            password = request.data.get('password')
            profile_picture = request.data.get('profile_picture')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            prefered_work_location = request.data.get('prefered_work_location')
            country = request.data.get('country')
            fcm_token = request.data.get('fcm_token')
            mobile_number = request.data.get('mobile_number')
            whatsapp_number = request.data.get('whatsapp_number')
            about = request.data.get('about')
            category = request.data.get('category')
            subcategory = request.data.get('subcategory')
            charge_type = request.data.get('charge_type')

            id_card_type = request.data.get('id_card_type')
            id_card_number = request.data.get('id_card_number')
            id_card = request.data.get('id_card')
            sunday_start_time = request.data.get('sunday_start_time')
            sunday_end_time = request.data.get('sunday_end_time')
            monday_start_time = request.data.get('monday_start_time')
            monday_end_time = request.data.get('monday_end_time')
            tuesday_start_time = request.data.get('tuesday_start_time')
            tuesday_end_time = request.data.get('tuesday_end_time')
            wednesday_start_time = request.data.get('wednesday_start_time')
            wednesday_end_time = request.data.get('wednesday_end_time')
            thursday_start_time = request.data.get('thursday_start_time')
            thursday_end_time = request.data.get('thursday_end_time')
            friday_start_time = request.data.get('friday_start_time')
            friday_end_time = request.data.get('friday_end_time')
            saturday_start_time = request.data.get('saturday_start_time')
            saturday_end_time = request.data.get('saturday_end_time')

            # Convert empty strings to None for time fields
            sunday_start_time = sunday_start_time if sunday_start_time else None
            sunday_end_time = sunday_end_time if sunday_end_time else None
            monday_start_time = monday_start_time if monday_start_time else None
            monday_end_time = monday_end_time if monday_end_time else None
            tuesday_start_time = tuesday_start_time if tuesday_start_time else None
            tuesday_end_time = tuesday_end_time if tuesday_end_time else None
            wednesday_start_time = wednesday_start_time if wednesday_start_time else None
            wednesday_end_time = wednesday_end_time if wednesday_end_time else None
            thursday_start_time = thursday_start_time if thursday_start_time else None
            thursday_end_time = thursday_end_time if thursday_end_time else None
            friday_start_time = friday_start_time if friday_start_time else None
            friday_end_time = friday_end_time if friday_end_time else None
            saturday_start_time = saturday_start_time if saturday_start_time else None
            saturday_end_time = saturday_end_time if saturday_end_time else None
            
            
      
            country_instance = Country.objects.get(id=country)
            prefered_work_location_instance = District.objects.get(id=prefered_work_location)

            


            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=email, name=name, email=email, password=password, country=country_instance, 
                                                   fcm_token=fcm_token, mobile_number=mobile_number,whatsapp_number=whatsapp_number,about=about,user_type="Employee",
                                                  profile_picture=profile_picture,charge=charge_type,first_name=first_name,last_name=last_name,prefered_work_location=prefered_work_location_instance,
                                                  id_card_type=id_card_type,id_card_number=id_card_number,id_card=id_card)

            print("customer creation")

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



            category_ids = request.data.get("category", "")
            category_ids = [int(id.strip()) for id in category_ids.split(",") if id.strip().isdigit()]

            subcategory_ids = request.data.get("subcategory", "")
            subcategory_ids = [int(id.strip()) for id in subcategory_ids.split(",") if id.strip().isdigit()]

            wages = request.data.get("wages", "")
            # Split the wages by commas and strip any leading/trailing whitespace
            wages = [wage.strip() for wage in wages.split(",") if wage.strip()]
            print("customer creation 2")

            for subcategory_id, wage in zip(subcategory_ids, wages):
                EmployyeWages.objects.create(
                    user=user,
                    subcategory_id=subcategory_id,
                    wages=wage  # Store the full wage string, including the currency
                )
            print("customer creation 3")
 

            if category_ids:
                category = []
                for i in category_ids:
                    catgry = Category.objects.get(id=i)
                    category.append(catgry)
                user.category.set(category)

            if subcategory_ids:
                subcategory = []
                for i in subcategory_ids:
                    subcatgry = SubCategory.objects.get(id=i)
                    subcategory.append(subcatgry)
                user.subcategory.set(subcategory)
            access_token = RefreshToken.for_user(user).access_token

            print("customer creation 4")


            EmployeeWorkSchedule.objects.create(user=user,sunday_start_time=sunday_start_time,sunday_end_time=sunday_end_time,
                                                monday_start_time=monday_start_time,monday_end_time=monday_end_time,
                                                tuesday_start_time=tuesday_start_time,tuesday_end_time=tuesday_end_time,
                                                wednesday_start_time=wednesday_start_time,wednesday_end_time=wednesday_end_time,
                                                thursday_start_time=thursday_start_time,
                                                thursday_end_time=thursday_end_time,friday_start_time=friday_start_time,
                                                friday_end_time=friday_end_time,saturday_start_time=saturday_start_time,
                                                saturday_end_time=saturday_end_time)
            print("customer creation 5")

            # Call the utility function to create time slots for each day
            if sunday_start_time and sunday_end_time:
                create_time_slots(user, "Sunday", sunday_start_time, sunday_end_time)
            if monday_start_time and monday_end_time:
                create_time_slots(user, "Monday", monday_start_time, monday_end_time)
            if tuesday_start_time and tuesday_end_time:
                create_time_slots(user, "Tuesday", tuesday_start_time, tuesday_end_time)
            if wednesday_start_time and wednesday_end_time:
                create_time_slots(user, "Wednesday", wednesday_start_time, wednesday_end_time)
            if thursday_start_time and thursday_end_time:
                create_time_slots(user, "Thursday", thursday_start_time, thursday_end_time)
            if friday_start_time and friday_end_time:
                create_time_slots(user, "Friday", friday_start_time, friday_end_time)
            if saturday_start_time and saturday_end_time:
                create_time_slots(user, "Saturday", saturday_start_time, saturday_end_time)

            print("Time slots created")

            return Response({
                'message': 'Employee created successfully',
                'access_token': str(access_token),
                'refresh_token': str(RefreshToken.for_user(user).access_token),
                'user_details': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)







# class EmployeeLogin(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if CustomUser.objects.filter(email=email).exists():
#             user = CustomUser.objects.get(email=email,user_type="Employee")
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


class EmployeeLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        fcm_token = request.data.get('fcm_token')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email, user_type="Employee").exists():
            user = CustomUser.objects.get(email=email, user_type="Employee")
            # Check if user is active
            if not user.status == 'Active':
                return Response({"error": "Your account is Disabled by Admin. Please contact support."}, status=status.HTTP_403_FORBIDDEN)
            
            # Check password first
            if user.check_password(password):
                # Update FCM token if provided
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




@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True,context={'request':request})
    return Response(serializer.data)



@api_view(['POST'])
def subcategories_by_category(request):
    # Extract category IDs from the request body (JSON data)
    category_ids = request.data.get('category_ids', [])
    
    if not category_ids:
        return Response({"error": "Category IDs are required"}, status=400)

    # Fetch subcategories based on the provided category IDs
    subcategories = SubCategory.objects.filter(service__id__in=category_ids)
    sub_category_list = []
    for i in subcategories:
        sub_category_list.append({
            "id": i.id,
            "name": i.name,
            "logo": request.build_absolute_uri(i.logo.url) if i.logo else None,
        })
    return Response(sub_category_list)







@api_view(['POST'])
def requested_category_api(request):
    if request.method == 'POST':
        serializer = RequestedCategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)



@api_view(['POST'])
def employee_detail_api(request):
    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
        employee = get_object_or_404(CustomUser, id=employee_id)
        serializer = EmployeeSerializer(employee,context={'request':request})
        return Response(serializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def employee_home(request):
    user = request.user
    print(user)
    if request.method == 'GET':
        total_booking = Booking.objects.filter(employee=user, status__in=['Pending', 'Active']).count()
        completed_booking = Booking.objects.filter(employee=user, status='Completed').count()
        active_work_orders = Booking.objects.filter(employee=user, status='Pending')
        active_work_orders_serializer = BookingSerializer(active_work_orders, many=True,context={'request':request})
        return Response({'employee_dashboard':
                         {'total_booking': total_booking,
                         'completed_booking': completed_booking,
                         },
                         'active_work_orders': active_work_orders_serializer.data,
                        })


    if request.method == 'POST':
        booking_id = request.data.get('booking_id')
        status = request.data.get('status')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = status
        booking.save()
        return Response({'message': 'Booking status updated successfully'})
    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_profile_api(request):
    user = request.user
    # CustomUser data
    user_data = {

        'id': user.id,
        'name': user.name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'mobile_number': user.mobile_number,
        'whatsapp_number': user.whatsapp_number,
        'email': user.email,
        'about': user.about,
        'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
        'category': [
            {'id': category.id, 'name': category.name}
            for category in user.category.all()
        ],
        'subcategory': [
            {'id': subcategory.id, 'name': subcategory.name}
            for subcategory in user.subcategory.all()
        ],
        'charge': user.charge,
        'date_of_birth': user.date_of_birth,
        'gender': user.gender,
        'approval_status': user.approval_status,
        'country': user.country.name if user.country else None,
        'state': [
            {'id': state.id, 'name': state.name}
            for state in user.state.all()
        ],
        'district': [
            {'id': district.id, 'name': district.name}
            for district in user.district.all()
        ],
        'prefered_work_location': user.prefered_work_location.name if user.prefered_work_location else None,
        'id_card_type': user.id_card_type,
        'id_card_number': user.id_card_number,
        'id_card': request.build_absolute_uri(user.id_card.url) if user.id_card else None,
    }
    
    # EmployeeWorkSchedule data
    work_schedule = EmployeeWorkSchedule.objects.filter(user=user).first()
    if work_schedule:
        user_data['work_schedule'] = {
            'sunday_start_time': work_schedule.sunday_start_time,
            'sunday_end_time': work_schedule.sunday_end_time,
            'monday_start_time': work_schedule.monday_start_time,
            'monday_end_time': work_schedule.monday_end_time,
            'tuesday_start_time': work_schedule.tuesday_start_time,
            'tuesday_end_time': work_schedule.tuesday_end_time,
            'wednesday_start_time': work_schedule.wednesday_start_time,
            'wednesday_end_time': work_schedule.wednesday_end_time,
            'thursday_start_time': work_schedule.thursday_start_time,
            'thursday_end_time': work_schedule.thursday_end_time,
            'friday_start_time': work_schedule.friday_start_time,
            'friday_end_time': work_schedule.friday_end_time,
            'saturday_start_time': work_schedule.saturday_start_time,
            'saturday_end_time': work_schedule.saturday_end_time,
        }
    
    # EmployyeWages data
    wages = EmployyeWages.objects.filter(user=user)
    user_data['employee_wages'] = [
        {
            'subcategory': wage.subcategory.name if wage.subcategory else None,
            'wages': wage.wages,
        }
        for wage in wages
    ]

    return JsonResponse(user_data)







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_employee_profile(request):
    user = request.user
    email = request.POST.get('email', '').strip()
    # Update CustomUser fields
    if request.POST.get('name') != '':
        user.name = request.POST.get('name', user.name)


    if request.POST.get('first_name') != '':
        user.first_name = request.POST.get('first_name', user.first_name)
        
    if request.POST.get('last_name') != '':
        user.last_name = request.POST.get('last_name', user.last_name)
        
    if request.POST.get('mobile_number') != '':
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
        
    if request.POST.get('whatsapp_number') != '':
        user.whatsapp_number = request.POST.get('whatsapp_number', user.whatsapp_number)
        
    # Check if the new email is already taken by another user
    if email and email != user.email:
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."},status=status.HTTP_400_BAD_REQUEST)
        
    if request.POST.get('about') != '':
        user.about = request.POST.get('about', user.about)
        
    if request.POST.get('charge') != '':
        user.charge = request.POST.get('charge', user.charge)
        
    if request.POST.get('date_of_birth') != '':
        user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        
    if request.POST.get('gender') != '':
        user.gender = request.POST.get('gender', user.gender)
        
    if request.POST.get('approval_status') != '':
        user.approval_status = request.POST.get('approval_status', user.approval_status)
        
    if request.POST.get('country_id') != '':
        user.country_id = request.POST.get('country_id', user.country_id)
        
        
    if request.POST.get('prefered_work_location_id') != '':
        user.prefered_work_location_id = request.POST.get('prefered_work_location_id', user.prefered_work_location_id)
        
    if request.POST.get('id_card_type') != '':
        user.id_card_type = request.POST.get('id_card_type', user.id_card_type)
        
    if request.POST.get('id_card_number') != '':
        user.id_card_number = request.POST.get('id_card_number', user.id_card_number)
    
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    
    if 'id_card' in request.FILES:
        user.id_card = request.FILES['id_card']

    # Save the updated CustomUser model
    user.save()

    # Update EmployeeWorkSchedule fields
    work_schedule, created = EmployeeWorkSchedule.objects.get_or_create(user=user)

    if request.POST.get('sunday_start_time') != '':
        work_schedule.sunday_start_time = request.POST.get('sunday_start_time', work_schedule.sunday_start_time)
        
    if request.POST.get('sunday_end_time') != '':
        work_schedule.sunday_end_time = request.POST.get('sunday_end_time', work_schedule.sunday_end_time)

    if request.POST.get('monday_start_time') != '':
        work_schedule.monday_start_time = request.POST.get('monday_start_time', work_schedule.monday_start_time)

    if request.POST.get('monday_end_time') != '':
        work_schedule.monday_end_time = request.POST.get('monday_end_time', work_schedule.monday_end_time)

    if request.POST.get('tuesday_start_time') != '':
        work_schedule.tuesday_start_time = request.POST.get('tuesday_start_time', work_schedule.tuesday_start_time)

    if request.POST.get('tuesday_end_time') != '':
        work_schedule.tuesday_end_time = request.POST.get('tuesday_end_time', work_schedule.tuesday_end_time)

    if request.POST.get('wednesday_start_time') != '':
        work_schedule.wednesday_start_time = request.POST.get('wednesday_start_time', work_schedule.wednesday_start_time)

    if request.POST.get('wednesday_end_time') != '':
        work_schedule.wednesday_end_time = request.POST.get('wednesday_end_time', work_schedule.wednesday_end_time)

    if request.POST.get('thursday_start_time') != '':
        work_schedule.thursday_start_time = request.POST.get('thursday_start_time', work_schedule.thursday_start_time)

    if request.POST.get('thursday_end_time') != '':
        work_schedule.thursday_end_time = request.POST.get('thursday_end_time', work_schedule.thursday_end_time)

    if request.POST.get('friday_start_time') != '':
        work_schedule.friday_start_time = request.POST.get('friday_start_time', work_schedule.friday_start_time)

    if request.POST.get('friday_end_time') != '':
        work_schedule.friday_end_time = request.POST.get('friday_end_time', work_schedule.friday_end_time)

    if request.POST.get('saturday_start_time') != '':
        work_schedule.saturday_start_time = request.POST.get('saturday_start_time', work_schedule.saturday_start_time)

    if request.POST.get('saturday_end_time') != '':
        work_schedule.saturday_end_time = request.POST.get('saturday_end_time', work_schedule.saturday_end_time)

    # Save the updated EmployeeWorkSchedule model
    work_schedule.save()

    sunday_start_time = request.data.get('sunday_start_time')
    sunday_end_time = request.data.get('sunday_end_time')
    monday_start_time = request.data.get('monday_start_time')
    monday_end_time = request.data.get('monday_end_time')
    tuesday_start_time = request.data.get('tuesday_start_time')
    tuesday_end_time = request.data.get('tuesday_end_time')
    wednesday_start_time = request.data.get('wednesday_start_time')
    wednesday_end_time = request.data.get('wednesday_end_time')
    thursday_start_time = request.data.get('thursday_start_time')
    thursday_end_time = request.data.get('thursday_end_time')
    friday_start_time = request.data.get('friday_start_time')
    friday_end_time = request.data.get('friday_end_time')
    saturday_start_time = request.data.get('saturday_start_time')
    saturday_end_time = request.data.get('saturday_end_time')

    # Convert empty strings to None for time fields
    sunday_start_time = sunday_start_time if sunday_start_time else None
    sunday_end_time = sunday_end_time if sunday_end_time else None
    monday_start_time = monday_start_time if monday_start_time else None
    monday_end_time = monday_end_time if monday_end_time else None
    tuesday_start_time = tuesday_start_time if tuesday_start_time else None
    tuesday_end_time = tuesday_end_time if tuesday_end_time else None
    wednesday_start_time = wednesday_start_time if wednesday_start_time else None
    wednesday_end_time = wednesday_end_time if wednesday_end_time else None
    thursday_start_time = thursday_start_time if thursday_start_time else None
    thursday_end_time = thursday_end_time if thursday_end_time else None
    friday_start_time = friday_start_time if friday_start_time else None
    friday_end_time = friday_end_time if friday_end_time else None
    saturday_start_time = saturday_start_time if saturday_start_time else None
    saturday_end_time = saturday_end_time if saturday_end_time else None

 # Call the utility function to create time slots for each day
    if sunday_start_time and sunday_end_time:
        create_time_slots(user, "Sunday", sunday_start_time, sunday_end_time)
    if monday_start_time and monday_end_time:
        create_time_slots(user, "Monday", monday_start_time, monday_end_time)
    if tuesday_start_time and tuesday_end_time:
        create_time_slots(user, "Tuesday", tuesday_start_time, tuesday_end_time)
    if wednesday_start_time and wednesday_end_time:
        create_time_slots(user, "Wednesday", wednesday_start_time, wednesday_end_time)
    if thursday_start_time and thursday_end_time:
        create_time_slots(user, "Thursday", thursday_start_time, thursday_end_time)
    if friday_start_time and friday_end_time:
        create_time_slots(user, "Friday", friday_start_time, friday_end_time)
    if saturday_start_time and saturday_end_time:
        create_time_slots(user, "Saturday", saturday_start_time, saturday_end_time)

    category_ids = request.data.get("category", "")
    category_ids = [int(id.strip()) for id in category_ids.split(",") if id.strip().isdigit()]
    subcategory_ids = request.data.get("subcategory", "")
    subcategory_ids = [int(id.strip()) for id in subcategory_ids.split(",") if id.strip().isdigit()]

    state_ids = request.data.get("state", "")
    state_ids = [int(id.strip()) for id in state_ids.split(",") if id.strip().isdigit()]

    if state_ids:
        states = []
        for i in state_ids:
            try:
                statee = State.objects.get(id=i)
                states.append(statee)
            except State.DoesNotExist:
                pass  # Handle if category doesn't exist
        user.state.set(states)  # Use set to replace existing categories with the provided ones

    district_ids = request.data.get("district", "")
    district_ids = [int(id.strip()) for id in district_ids.split(",") if id.strip().isdigit()]

    if district_ids:
        district = []
        for i in district_ids:
            try:
                districtt = District.objects.get(id=i)
                district.append(districtt)
            except District.DoesNotExist:
                pass  # Handle if category doesn't exist
        user.district.set(district)  # Use set to replace existing categories with the provided ones



    # Handle category updates with create or update logic
    if category_ids:
        categories = []
        for i in category_ids:
            try:
                catgry = Category.objects.get(id=i)
                categories.append(catgry)
            except Category.DoesNotExist:
                pass  # Handle if category doesn't exist
        user.category.set(categories)  # Use set to replace existing categories with the provided ones

    # Handle subcategory updates with create or update logic
    if subcategory_ids:
        subcategories = []
        for i in subcategory_ids:
            try:
                subcatgry = SubCategory.objects.get(id=i)
                subcategories.append(subcatgry)
            except SubCategory.DoesNotExist:
                pass  # Handle if subcategory doesn't exist
        user.subcategory.set(subcategories)  # Use set to replace existing subcategories with the provided ones


    # Update EmployyeWages fields
    subcategory_ids = request.data.get("subcategory", "")
    subcategory_ids = [int(id.strip()) for id in subcategory_ids.split(",") if id.strip().isdigit()]

    wages = request.data.get("wages", "")
    wages = [int(id.strip()) for id in wages.split(",") if id.strip().isdigit()]
    print("customer creation 2")
    if wages:
        for subcategory_id, wage in zip(subcategory_ids, wages):
            # Use update_or_create to update the wage if it exists, or create it if not
            EmployyeWages.objects.update_or_create(
                user=user,
                subcategory_id=subcategory_id,
                defaults={'wages': wage}
            )

    return JsonResponse({'status': 'success', 'message': 'Profile and related data updated successfully'})



import calendar
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q


@api_view(['POST'])
def my_orders(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    # Get the filter option from request data (POST request)
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

    # Apply the date filter if provided
    query = Q(employee=request.user)
    if date_range:
        query &= Q(created_date__range=date_range)

    # Fetch bookings based on each status and apply the date filter
    pending_bookings = Booking.objects.filter(query & Q(status='Pending')).order_by('-id')
    accepted_bookings = Booking.objects.filter(query & Q(status='Accept')).order_by('-id')
    completed_bookings = Booking.objects.filter(query & Q(status='Completed')).order_by('-id')
    rejected_bookings = Booking.objects.filter(query & Q(status='Reject')).order_by('-id')

    # Serialize the bookings
    pending_serializer = BookingSerializer(pending_bookings, many=True, context={'request': request})
    accepted_serializer = BookingSerializer(accepted_bookings, many=True, context={'request': request})
    completed_serializer = BookingSerializer(completed_bookings, many=True, context={'request': request})
    rejected_serializer = BookingSerializer(rejected_bookings, many=True, context={'request': request})

    # Return the data in a structured response
    return Response({
        'pending_bookings': pending_serializer.data,
        'accepted_bookings': accepted_serializer.data,
        'completed_bookings': completed_serializer.data,
        'rejected_bookings': rejected_serializer.data,
    })




@api_view(['POST'])
def get_time_slots(request):
    try:
        # Parse the request data
        data = request.data
        user_id = data.get('employee_id')
        day = data.get('day')

        if not user_id or not day:
            return JsonResponse({'error': 'user_id and day are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the time slots based on user_id and day
        time_slots = EmployeeWorkTimeSlot.objects.filter(user_id=user_id, day=day)

        # Serialize the time slots data
        serializer = EmployeeWorkTimeSlotSerializer(time_slots, many=True)

        return JsonResponse({'time_slots': serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    







# @api_view(['POST'])
# def employee_all_reviews(request):
#     # Fetch the employee by ID from POST data
#     employee_id = request.data.get('employee_id')
    
#     # Validate employee existence
#     employee = get_object_or_404(CustomUser, id=employee_id)
    
#     # Fetch all reviews for the employee and apply initial ordering
#     reviews = Review.objects.filter(employee=employee)

#     # Fetch the filter parameter from the request
#     filter_type = request.data.get('filter', 'all')

#     # Initialize the rating field for distribution based on the filter
#     rating_field = 'average_rating'

#     # Apply filters and set the rating field based on the parameter received
#     if filter_type == 'timing':
#         reviews = reviews.order_by('-timing')
#         rating_field = 'timing'
#     elif filter_type == 'price':
#         reviews = reviews.order_by('-price')
#         rating_field = 'price'
#     elif filter_type == 'quality':
#         reviews = reviews.order_by('-service_quality')
#         rating_field = 'service_quality'
#     elif filter_type == 'behavior':
#         reviews = reviews.order_by('-behavior')
#         rating_field = 'behavior'
#     else:  # Default case: 'all' or no filter
#         reviews = reviews.order_by('-review_date')

#     # Prepare reviews list with required fields for the UI
#     reviews_list = [
#         {
#             'user_name': review.user.name if review.user else "Anonymous",
#             'profile_pic': request.build_absolute_uri(review.user.profile_picture.url) if review.user and review.user.profile_picture else None,
#             'review_date': review.review_date.strftime("%b %Y"),
#             'average_rating': review.average_rating,
#             'service_summary': review.service_summary,
#             'timing': review.timing,
#             'price': review.price,
#             'service_quality': review.service_quality,
#             'behavior': review.behavior,
#             'review': review.review,
#         }
#         for review in reviews
#     ]

#     # Calculate overall rating summary using aggregation
#     average_rating = reviews.aggregate(average_rating=Avg('average_rating'))['average_rating']
#     average_rating = round(average_rating, 1) if average_rating is not None else 0 

#     rating_summary = {
#         'total_reviews': reviews.count(),
#         'average_rating': average_rating,
#         'timing_avg': reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'],
#         'price_avg': reviews.aggregate(price_avg=Avg('price'))['price_avg'],
#         'service_quality_avg': reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'],
#         'behavior_avg': reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'],
#     }

#     # Calculate the count of reviews for each star rating based on the selected rating field
#     rating_distribution = {
#         '5_star': reviews.filter(**{f'{rating_field}__gte': 4.9}).count(),
#         '4_star': reviews.filter(**{f'{rating_field}__gte': 3.9, f'{rating_field}__lt': 4.9}).count(),
#         '3_star': reviews.filter(**{f'{rating_field}__gte': 2.9, f'{rating_field}__lt': 3.9}).count(),
#         '2_star': reviews.filter(**{f'{rating_field}__gte': 1.9, f'{rating_field}__lt': 2.9}).count(),
#         '1_star': reviews.filter(**{f'{rating_field}__lt': 1.9}).count(),
#     }

#     # Prepare the final response data to fit the UI
#     response_data = {
#         'employee': employee.name,
#         'rating_summary': {
#             'total_reviews': rating_summary['total_reviews'],
#             'average_rating': rating_summary['average_rating'],
#             'timing_avg': round(rating_summary['timing_avg'], 1) if rating_summary['timing_avg'] is not None else 0,
#             'price_avg': round(rating_summary['price_avg'], 1) if rating_summary['price_avg'] is not None else 0,
#             'service_quality_avg': round(rating_summary['service_quality_avg'], 1) if rating_summary['service_quality_avg'] is not None else 0,
#             'behavior_avg': round(rating_summary['behavior_avg'], 1) if rating_summary['behavior_avg'] is not None else 0,
#         },
#         'rating_distribution': rating_distribution,
#         'reviews': reviews_list,
#     }

#     # Return the response as JSON
#     return Response(response_data)


@api_view(['POST'])
def employee_all_reviews(request):
    # Fetch the employee by ID from POST data
    employee_id = request.data.get('employee_id')
    
    # Validate employee existence
    employee = get_object_or_404(CustomUser, id=employee_id)
    
    # Fetch all reviews for the employee and apply initial ordering
    reviews = Review.objects.filter(employee=employee)

    # Fetch the filter parameter from the request
    filter_type = request.data.get('filter', 'all')

    # Initialize the rating field for distribution and average calculation based on the filter
    rating_field = 'average_rating'

    # Apply filters and set the rating field based on the parameter received
    if filter_type == 'timing':
        reviews = reviews.order_by('-timing')
        rating_field = 'timing'
    elif filter_type == 'price':
        reviews = reviews.order_by('-price')
        rating_field = 'price'
    elif filter_type == 'quality':
        reviews = reviews.order_by('-service_quality')
        rating_field = 'service_quality'
    elif filter_type == 'behavior':
        reviews = reviews.order_by('-behavior')
        rating_field = 'behavior'
    else:  # Default case: 'all' or no filter
        reviews = reviews.order_by('-review_date')

    # Prepare reviews list with required fields for the UI
    reviews_list = [
        {
            'user_name': review.user.name if review.user else "Anonymous",
            'profile_pic': request.build_absolute_uri(review.user.profile_picture.url) if review.user and review.user.profile_picture else None,
            'review_date': review.review_date.strftime("%b %Y"),
            'average_rating': review.average_rating,
            'service_summary': review.service_summary,
            'timing': review.timing,
            'price': review.price,
            'service_quality': review.service_quality,
            'behavior': review.behavior,
            'review': review.review,
        }
        for review in reviews
    ]

    # Dynamically calculate the average based on the selected filter field
    filtered_avg = reviews.aggregate(filtered_avg=Avg(rating_field))['filtered_avg']
    filtered_avg = round(filtered_avg, 1) if filtered_avg is not None else 0

    # Calculate the rest of the average metrics
    rating_summary = {
        'total_reviews': reviews.count(),
        'average_rating': filtered_avg,  # Dynamic average based on filter
        'timing_avg': round(reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'], 1) if reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'] is not None else 0,
        'price_avg': round(reviews.aggregate(price_avg=Avg('price'))['price_avg'], 1) if reviews.aggregate(price_avg=Avg('price'))['price_avg'] is not None else 0,
        'service_quality_avg': round(reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'], 1) if reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'] is not None else 0,
        'behavior_avg': round(reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'], 1) if reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'] is not None else 0,
    }

    # Calculate the count of reviews for each star rating based on the selected rating field
    rating_distribution = {
        '5_star': reviews.filter(**{f'{rating_field}__gte': 4.9}).count(),
        '4_star': reviews.filter(**{f'{rating_field}__gte': 3.9, f'{rating_field}__lt': 4.9}).count(),
        '3_star': reviews.filter(**{f'{rating_field}__gte': 2.9, f'{rating_field}__lt': 3.9}).count(),
        '2_star': reviews.filter(**{f'{rating_field}__gte': 1.9, f'{rating_field}__lt': 2.9}).count(),
        '1_star': reviews.filter(**{f'{rating_field}__lt': 1.9}).count(),
    }

    # Prepare the final response data to fit the UI
    response_data = {
        'employee': employee.name,
        'rating_summary': rating_summary,
        'rating_distribution': rating_distribution,
        'reviews': reviews_list,
    }

    # Return the response as JSON
    return Response(response_data)



@api_view(['GET'])
def get_onboardings(request):
    onboardings = Onbaording.objects.all()
    serializer = OnboardingSerializer(onboardings, many=True, context={'request': request})
    return Response(serializer.data)





@api_view(['POST'])
def notification_history_api(request):
    print(request.user)
    user = request.user

    try:
        user = CustomUser.objects.get(id=user.id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    if user.user_type == 'User':
        notifications = Notification.objects.filter(user=user, user_type='User').order_by('-timestamp')[:10]
    elif user.user_type == 'Employee':
        notifications = Notification.objects.filter(employee=user, user_type='Employee').order_by('-timestamp')[:10]
    else:
        return Response({"error": "Invalid user type."}, status=400)

    notification_list = [{
        'title': notification.title,
        'description': notification.description,
        'timestamp': notification.timestamp,
        'is_read': notification.is_read
    } for notification in notifications]

    return Response(notification_list)








def get_currency_types(request):
    if request.method == 'GET':
        # Use values() to directly retrieve the 'id' and 'name' fields as dictionaries
        currency_list = list(Currency_Type.objects.values('id', 'name'))

        # Return as JSON response
        return JsonResponse({'currencies': currency_list}, status=200)
    







@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user  # Get the logged-in user
    user.delete()  # Delete the user account
    logout(request)  # Log the user out after deletion
    return Response({"detail": "Account deleted successfully."}, status=status.HTTP_200_OK)