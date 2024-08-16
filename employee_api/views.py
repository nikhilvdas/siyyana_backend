from django.shortcuts import render
from rest_framework.decorators import api_view
from siyyana_app.models import Country
from employee_api.serializers import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
def index(request):
    return render(request, 'user_api/index.html')



@api_view(['GET'])
def location_list_api(request):
    if request.method == 'GET':
        locations = Country.objects.all()
        serializer = LocationSerializer(locations, many=True,context={'request':request})
        return Response(serializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
