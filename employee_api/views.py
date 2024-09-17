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
        
        state_id = request.data.get('state_id')
        if state_id:
            state = State.objects.get(id=state_id)
            district = District.objects.filter(state=state)
            serializer = DistrictSerializer(district, many=True,context={'request':request})
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
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, '%H:%M').time()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, '%H:%M').time()
    
    current_time = start_time
    print('Entered create_time_slots function')

    while current_time < end_time:
        next_time = (datetime.combine(date.today(), current_time) + timedelta(hours=1)).time()
        print(f'Current time: {current_time}, Next time: {next_time}')
        
        # Ensure that the next time does not exceed the end time
        if next_time > end_time:
            next_time = end_time
        
        # Create the time slot for this interval
        EmployeeWorkTimeSlot.objects.create(
            user=user,
            day=day,
            start_time=current_time,
            end_time=next_time
        )
        
        # Move to the next 1-hour slot
        current_time = next_time
    
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
            state = request.data.get('state')
            district = request.data.get('district')
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
            
            
      
            country_instance = Country.objects.get(id=country)
            state_instance = State.objects.get(id=state)
            district_instance = District.objects.get(id=district)
            prefered_work_location_instance = District.objects.get(id=prefered_work_location)

            


            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=email, name=name, email=email, password=password, country=country_instance, state=state_instance, 
                                                  district=district_instance, fcm_token=fcm_token, mobile_number=mobile_number,whatsapp_number=whatsapp_number,about=about,user_type="Employee",
                                                  profile_picture=profile_picture,charge=charge_type,first_name=first_name,last_name=last_name,prefered_work_location=prefered_work_location_instance,
                                                  id_card_type=id_card_type,id_card_number=id_card_number,id_card=id_card)

            print("customer creation")
            category_ids = request.data.get("category", "")
            category_ids = [int(id.strip()) for id in category_ids.split(",") if id.strip().isdigit()]

            subcategory_ids = request.data.get("subcategory", "")
            subcategory_ids = [int(id.strip()) for id in subcategory_ids.split(",") if id.strip().isdigit()]

            wages = request.data.get("wages", "")
            wages = [int(id.strip()) for id in wages.split(",") if id.strip().isdigit()]
            print("customer creation 2")

            for subcategory_id, wage in zip(subcategory_ids, wages):
                EmployyeWages.objects.create(
                    user=user,
                    subcategory_id=subcategory_id,
                    wages=wage
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







class EmployeeLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email,user_type="Employee")
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
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response(serializer.data)







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
        total_booking = Booking.objects.filter(employee=user).count()
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
        'first_name': user.first_name,
        'last_name': user.last_name,
        'mobile_number': user.mobile_number,
        'whatsapp_number': user.whatsapp_number,
        'email': user.email,
        'about': user.about,
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
        'state': user.state.name if user.state else None,
        'district': user.district.name if user.district else None,
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
    first_name = user.first_name
    
    # Update CustomUser fields
    user.first_name = request.POST.get('first_name', first_name)
    user.last_name = request.POST.get('last_name', user.last_name)
    user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
    user.whatsapp_number = request.POST.get('whatsapp_number', user.whatsapp_number)
    user.email = request.POST.get('email', user.email)
    user.about = request.POST.get('about', user.about)
    user.charge = request.POST.get('charge', user.charge)
    user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
    user.gender = request.POST.get('gender', user.gender)
    user.approval_status = request.POST.get('approval_status', user.approval_status)
    user.country_id = request.POST.get('country_id', user.country_id)
    user.state_id = request.POST.get('state_id', user.state_id)
    user.district_id = request.POST.get('district_id', user.district_id)
    user.prefered_work_location_id = request.POST.get('prefered_work_location_id', user.prefered_work_location_id)
    user.id_card_type = request.POST.get('id_card_type', user.id_card_type)
    user.id_card_number = request.POST.get('id_card_number', user.id_card_number)
    
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    
    if 'id_card' in request.FILES:
        user.id_card = request.FILES['id_card']

    # Save the updated CustomUser model
    user.save()

    # Update EmployeeWorkSchedule fields
    work_schedule, created = EmployeeWorkSchedule.objects.get_or_create(user=user)
    work_schedule.sunday_start_time = request.POST.get('sunday_start_time', work_schedule.sunday_start_time)
    work_schedule.sunday_end_time = request.POST.get('sunday_end_time', work_schedule.sunday_end_time)
    work_schedule.monday_start_time = request.POST.get('monday_start_time', work_schedule.monday_start_time)
    work_schedule.monday_end_time = request.POST.get('monday_end_time', work_schedule.monday_end_time)
    work_schedule.tuesday_start_time = request.POST.get('tuesday_start_time', work_schedule.tuesday_start_time)
    work_schedule.tuesday_end_time = request.POST.get('tuesday_end_time', work_schedule.tuesday_end_time)
    work_schedule.wednesday_start_time = request.POST.get('wednesday_start_time', work_schedule.wednesday_start_time)
    work_schedule.wednesday_end_time = request.POST.get('wednesday_end_time', work_schedule.wednesday_end_time)
    work_schedule.thursday_start_time = request.POST.get('thursday_start_time', work_schedule.thursday_start_time)
    work_schedule.thursday_end_time = request.POST.get('thursday_end_time', work_schedule.thursday_end_time)
    work_schedule.friday_start_time = request.POST.get('friday_start_time', work_schedule.friday_start_time)
    work_schedule.friday_end_time = request.POST.get('friday_end_time', work_schedule.friday_end_time)
    work_schedule.saturday_start_time = request.POST.get('saturday_start_time', work_schedule.saturday_start_time)
    work_schedule.saturday_end_time = request.POST.get('saturday_end_time', work_schedule.saturday_end_time)

    # Save the updated EmployeeWorkSchedule model
    work_schedule.save()

    # Update EmployyeWages fields
    wages_data = request.POST.getlist('wages_data[]', [])
    for wage_data in wages_data:
        subcategory_id = wage_data.get('subcategory_id')
        wages_amount = wage_data.get('wages')

        if subcategory_id and wages_amount:
            wages, created = EmployyeWages.objects.get_or_create(user=user, subcategory_id=subcategory_id)
            wages.wages = wages_amount
            # Save the updated EmployyeWages model
            wages.save()

    return JsonResponse({'status': 'success', 'message': 'Profile and related data updated successfully'})



import calendar
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q


@api_view(['GET'])
def my_orders(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    # Get the filter option from query parameters
    date_filter = request.GET.get('filter', 'All')

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
        query &= Q(date__range=date_range)

    # Fetch bookings based on each status and apply the date filter
    pending_bookings = Booking.objects.filter(query & Q(status='Pending'))
    accepted_bookings = Booking.objects.filter(query & Q(status='Accept'))
    completed_bookings = Booking.objects.filter(query & Q(status='Completed'))
    rejected_bookings = Booking.objects.filter(query & Q(status='Reject'))

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
    







@api_view(['POST'])
def employee_all_reviews(request):
    # Fetch the employee by ID from POST data
    employee_id = request.data.get('employee_id')
    
    # Validate employee existence
    employee = get_object_or_404(CustomUser, id=employee_id)
    
    # Fetch all reviews for the employee and order by the latest review date
    reviews = Review.objects.filter(employee=employee).order_by('-review_date')

    # Fetch the filter parameter from the request
    filter_type = request.data.get('filter', 'all')

    # Apply filters based on the parameter received
    if filter_type == 'timing':
        reviews = Review.objects.filter(employee=employee).order_by('-timing')
    elif filter_type == 'price':
        reviews = Review.objects.filter(employee=employee).order_by('-price')
    elif filter_type == 'quality':
        reviews = Review.objects.filter(employee=employee).order_by('-service_quality')
    elif filter_type == 'behavior':
        reviews = Review.objects.filter(employee=employee).order_by('-behavior')
    else:  # Default case: 'all' or no filter
        reviews = Review.objects.filter(employee=employee).order_by('-review_date')
    
    # Create a list of reviews with required fields
    reviews_list = [
        {
            'user_name': review.user.name if review.user else "Anonymous",
            'profile_pic': request.build_absolute_uri(review.user.profile_picture.url),
            'review_date': review.review_date.strftime("%b %Y"),
            'average_rating': review.average_rating,
            'service_summary': review.service_summary,
            'review': review.review,
        }
        for review in reviews
    ]
    
    # Calculate overall rating summary using aggregation
    rating_summary = {
        'total_reviews': reviews.count(),
        'average_rating': reviews.aggregate(average_rating=Avg('average_rating'))['average_rating'],
        'timing_avg': reviews.aggregate(timing_avg=Avg('timing'))['timing_avg'],
        'price_avg': reviews.aggregate(price_avg=Avg('price'))['price_avg'],
        'service_quality_avg': reviews.aggregate(service_quality_avg=Avg('service_quality'))['service_quality_avg'],
        'behavior_avg': reviews.aggregate(behavior_avg=Avg('behavior'))['behavior_avg'],
    }

    # Calculate the count of reviews for each star rating (1 to 5)
    rating_distribution = {

        '5_star': reviews.filter(average_rating__gte=4.9).count(),  # 4.9 to 5.0
        '4_star': reviews.filter(average_rating__gte=3.9, average_rating__lt=4.9).count(),  # 3.9 to <4.9
        '3_star': reviews.filter(average_rating__gte=2.9, average_rating__lt=3.9).count(),  # 2.9 to <3.9
        '2_star': reviews.filter(average_rating__gte=1.9, average_rating__lt=2.9).count(),  # 1.9 to <2.9
        '1_star': reviews.filter(average_rating__lt=1.9).count()# less than 1.9
    }

    # Prepare the final response data
    response_data = {
        'employee': employee.name,
        'rating_summary': rating_summary,
        'rating_distribution': rating_distribution,
        'reviews': reviews_list,
    }
    
    # Return the response as JSON
    return Response(response_data)