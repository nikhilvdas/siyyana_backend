from django.shortcuts import render
from rest_framework.decorators import api_view
from siyyana_app.models import Country
from employee_api.serializers import *
from rest_framework.response import Response
from rest_framework import status
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
