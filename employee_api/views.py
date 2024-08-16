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
            id_card_type = request.data.get('id_card_type')
            id_card_number = request.data.get('id_card_number')
            id_card = request.data.get('id_card')
            sunday_start_time = request.data.get('sunday_start_time')
            sunday_end_time = request.data.get('sunday_end_time')
            
            
      
            country_instance = Country.objects.get(id=country)
            state_instance = State.objects.get(id=state)
            district_instance = District.objects.get(id=district)
            prefered_work_location_instance = District.objects.get(id=prefered_work_location)

            


            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=email, name=name, email=email, password=password, country=country_instance, state=state_instance, 
                                                  district=district_instance, fcm_token=fcm_token, mobile_number=mobile_number,user_type="Employee",
                                                  profile_picture=profile_picture,first_name=first_name,last_name=last_name,prefered_work_location=prefered_work_location_instance,
                                                  id_card_type=id_card_type,id_card_number=id_card_number,id_card=id_card)
            access_token = RefreshToken.for_user(user).access_token

            EmployeeWorkSchedule.objects.create(user=user,sunday_start_time=sunday_start_time,sunday_end_time=sunday_end_time)
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



