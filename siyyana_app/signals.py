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