from django.shortcuts import render
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

            category_ids = request.data.get("category", "")
            category_ids = [int(id.strip()) for id in category_ids.split(",") if id.strip().isdigit()]

            subcategory_ids = request.data.get("subcategory", "")
            subcategory_ids = [int(id.strip()) for id in subcategory_ids.split(",") if id.strip().isdigit()]

            wages = request.data.get("wages", "")
            wages = [int(id.strip()) for id in wages.split(",") if id.strip().isdigit()]

            for subcategory_id, wage in zip(subcategory_ids, wages):
                EmployyeWages.objects.create(
                    user=user,
                    subcategory_id=subcategory_id,
                    wages=wage
                )


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

          

            EmployeeWorkSchedule.objects.create(user=user,sunday_start_time=sunday_start_time,sunday_end_time=sunday_end_time,
                                                monday_start_time=monday_start_time,monday_end_time=monday_end_time,
                                                tuesday_start_time=tuesday_start_time,tuesday_end_time=tuesday_end_time,
                                                wednesday_start_time=wednesday_start_time,wednesday_end_time=wednesday_end_time,
                                                thursday_start_time=thursday_start_time,
                                                thursday_end_time=thursday_end_time,friday_start_time=friday_start_time,
                                                friday_end_time=friday_end_time,saturday_start_time=saturday_start_time,
                                                saturday_end_time=saturday_end_time)
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







