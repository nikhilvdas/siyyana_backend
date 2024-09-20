from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# from .views import windows_notification_view
from django.contrib.auth import get_user_model
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from django.conf import settings
import json
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking


service_account_info =  {

    "type": "service_account",
    "project_id": "siyyana-86b0a",
    "private_key_id": "a5d2b7ab10be39d22c311e1615560be9c668cbb0",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC3ueSFSgaz66cM\nN3HNZLKC+tA/NgPVdcTD/Lm0gTnF2AOEM/esHLoPc+UbL79mnJm+3hGTOU2RG2Sy\nohOgyF9Ga/hZNOGQ148Ve8YRiVIb3nBQC4+2xFSbVZPAy1AXjgjG0S0lnc+Wo9Py\nGcO4kyMPCj8duaAG3K9t17203ASGwWPHMmwMTdaTfblY7ibnZtfC+B+btYMt4PVG\naGRkd50qgeteVDRAXnS3FJh9SZXygke2Fl6erYds/9zEzQzYdoQIGgqHfqdvyZ/G\ngRJcqgDzSC60eusKZA3AV/KE/i6Ni1ORYjy6cmCNC7+4dWEIj+pr9odk1DJ8HUzg\nBKuETeV7AgMBAAECggEAVfv+arEH7QlzHyENtioT73/RmVu+tJaO1YiAIu29q42a\nq7MkjRzOqS+8wBn7EltlCvJkOEo/tpMi8AUxeXR9PniGfL1mecKgeNX6Dzf8wQU7\n/AJFKqy8ygvlf/vHCpcTHXVFE09FmYMnzKzpMAdQh5fsjQ1USxHaWmZ3Jt83kRbD\nC4Fc8udyZkhi7gqWYyUz7RtddR2j7+IDc0Bw3FQq17FbIl8CI74UT7l4EQdOTxU6\nzOlYtidzK8LjYRVt9PHhDJtGEOxnh5EBrB3abXZlLLzkZYqSrbbyTvU119brKnHO\nciBSjUutkMZVLwpTinQCGg7uW6Z30Xg+9dfS7KHEXQKBgQDZrrV2l/JZZg0h5h80\nz8eRPEP7/YG6cDBkA+9mx/0XAPoheKD4XMuT3qYdhEbsNGFwPq8414na5SF2FXPi\n/yQAXjNrjHWyhIyuivhSTR5rafuahJEJmkdXdfwt917Qg6AGlNu6r2PkDkxcT3xm\nqGbqUrINFBWSiZ9EQ6v94m285wKBgQDYEQgCBJk1eZHzaTJ9rWhr79Rn/ROFMDRK\nDak2MbSkwNv+brcbTEQw7Xu5TfD+ro/NGD49g+6RCiyKO6RoLGE7wjQFXIbSjnqT\nO64WhhV4tNRuAbDdH+N8+t27o4NjyVWGBMlGP2/3Y7fhh/NX7NcWV3LfYOJRpAr9\ndpWcFpzMTQKBgQCSg/xRsV4GfCDUsz5H3p5Vi/m6T1wU79QyTU/Cn1MjO54gD0BR\nSqwfgBnQ/ip6a5s14IsxuClqcxS9lRzmKZLCyKTVe7nwiTTjelg/lPanl7MowpeY\nngXswVYWXkysDhwUsfbfRZP3eQQ+kaWKt0hl6Xk8Qktu0UCowt+tx8zS+wKBgDIg\n+W+ma3lZpEAKBxnbcp+gO/KIZ8/92BPaSYj2TUfwKtpEC518u1Fyt8LNT313OIvH\n9SDGjEIAT0cfAUzeBw0bSIB58BnHzq58KS62myKvKZ4ALG2RKXFkrq8LB7/OBVab\no6r1qt+FtjLQHOgoXdqkHVWwH7H7UkVuDtXw9R39AoGAE7dVAZjWMHIE1UZ2G2xG\n746xZjErTAkh1LzuJjxhafxsGj3yqraU5j8Xc9glOjrqu68poU3fri/BWuYrqEYc\np/1eqjWXi+UEEZTAby5toWoTmmSdQCEAglIwK0Bu3yQoXb45Q2XYw9Agg5N2Lz1U\nG8cmmf23bHprvplFcK1fwsw=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-lqnuq@siyyana-86b0a.iam.gserviceaccount.com",
    "client_id": "111549999066202189830",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-lqnuq%40siyyana-86b0a.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}





cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# Your Firebase project ID
project_id = 'siyyana-86b0a'

def get_access_token():
    """Retrieve a valid OAuth 2.0 access token that can be used to authorize requests."""
    SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token






def send_firebase_notification(title, description, fcm_token):
    try:
        access_token = get_access_token()
        print(f"Access token: {access_token}")
        if not access_token:
            print("Failed to obtain access token")
            return

        api_url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        data = {
            'message': {
                'notification': {
                    'title': title,
                    'body': description,
                },
                'token': fcm_token,  # Send to a specific FCM token
            }
        }

        print(f"Sending notification to token: {fcm_token}")
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            print(f'Firebase push notification sent successfully to {fcm_token}')
        else:
            print(f'Failed to send Firebase push notification to {fcm_token}. Status code: {response.status_code}, Response: {response.text}')

    except Exception as e:
        print(f'Error sending Firebase push notification: {e}')








# Pre-save signal to detect if the booking was rescheduled
@receiver(pre_save, sender=Booking)
def booking_rescheduled(sender, instance, **kwargs):
    print('booking reshedule')
    if instance.pk:  # Check if this is an update (i.e., existing booking)
        previous_booking = Booking.objects.get(pk=instance.pk)
        # Check if the date or time has changed
        if (previous_booking.date != instance.date) or (previous_booking.start_time != instance.start_time) or (previous_booking.end_time != instance.end_time):
            # Notify the user about the rescheduled booking
            send_firebase_notification(
                title="📆 Service Rescheduled",
                description=f"Your service for {instance.service.subcategory.name} has been rescheduled by {instance.employee.name}. The new date is {instance.date} at {instance.start_time}.",
                fcm_token=instance.user.fcm_token
            )




# Post-save signal to detect booking creation or status changes
@receiver(post_save, sender=Booking)
def booking_notifications(sender, instance, created, **kwargs):

    if created:
        # Send notification to the employee about the new booking
        send_firebase_notification(
            title="🚨 Service Alert",
            description=f"You have a new service request for {instance.service.subcategory.name} from {instance.user.name}. Check the app to view the details.",
            fcm_token=instance.employee.fcm_token
        )
    else:
        # Status change notifications
        if instance.status == 'Accept':
            send_firebase_notification(
                title="Booking Accepted",
                description=f"{instance.employee.name} has accepted your booking for {instance.service.subcategory.name}! Check the app for details and any additional instructions.",
                fcm_token=instance.user.fcm_token
            )
        elif instance.status == 'Completed':
            send_firebase_notification(
                title="🎊 Service Successfully Completed",
                description=f"The service for {instance.service.subcategory.name} has been completed by {instance.employee.name}. Thank you!",
                fcm_token=instance.user.fcm_token
            )
        elif instance.status == 'Reject':
            send_firebase_notification(
                title="❌ Booking Rejected",
                description=f"Your booking for {instance.service.subcategory.name} has been rejected by {instance.employee.name}. Please check the app for details.",
                fcm_token=instance.user.fcm_token
            )
        elif instance.status == 'Cancelled':
            send_firebase_notification(
                title="❌ Booking Cancelled",
                description=f"Your upcoming service for {instance.service.subcategory.name} has been cancelled by {instance.user.name}. Review the app for updates.",
                fcm_token=instance.employee.fcm_token
            )