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
            # country = request.data.get('country')
            # state = request.data.get('state')
            # district = request.data.get('district')
            fcm_token = request.data.get('fcm_token')
            mobile_number = request.data.get('mobile_number')
            whatsapp_number = request.data.get('whatsapp_number')
            # country_instance = Country.objects.get(id=country)
            # state_instance = State.objects.get(id=state)
            # district_instance = District.objects.get(id=district)
            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(username=email, name=name, email=email, password=password,
                                                   fcm_token=fcm_token, mobile_number=mobile_number,whatsapp_number=whatsapp_number,user_type="User")
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




@api_view(['GET'])
def category_with_subcategory_and_employees(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)





@api_view(['POST'])
def booking_api(request):
    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
        employee = CustomUser.objects.get(id=employee_id)
        user_id = request.data.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        service_id = request.data.get("service_id", "")
        booking_date = request.data.get('booking_date')
        data = Booking.objects.create(employee=employee, user=user, date=booking_date)

        service_id = [int(id.strip()) for id in service_id.split(",") if id.strip().isdigit()]
        service = []
        for i in service_id:
            services = EmployyeWages.objects.get(id=i)
            service.append(services)
        data.service.set(service)
    return Response({'message': 'Booking created successfully'},status=status.HTTP_200_OK)





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
        category = Category.objects.get(name__icontains=category_name)
        users = CustomUser.objects.filter(category=category).distinct()

        user_data = []
        for user in users:
            user_data.append({
                'name': user.name,
                'mobile_number': user.mobile_number,
                'whatsapp_number': user.whatsapp_number,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'about': user.about,
            })

        return JsonResponse({'users': user_data}, status=200)

    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found.'}, status=404)
    


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def save_employee(request):
    user = request.user

    if request.method == 'GET':
        saved_employees = Saved_Employees.objects.filter(user=user)
        employees_list = []
        for saved in saved_employees:
            employees_list.append({

                "id": saved.employee.id,
                "employee_name": saved.employee.name,
                "employee_mobile": saved.employee.mobile_number,
                "employee_whatsapp": saved.employee.whatsapp_number,
                "employee_profile_picture": request.build_absolute_uri(saved.employee.profile_picture.url) if saved.employee.profile_picture else None,
                "employee_about": saved.employee.about,
                
            })
        return JsonResponse({"saved_employees": employees_list}, status=200)

    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
        print(employee_id)
        print(request.user)
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
