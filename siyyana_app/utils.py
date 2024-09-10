from django.db.models import Count
from .models import Booking

def top_booked_employees(limit=5):
    # Annotate employees with booking count and order by most booked
    top_employees = Booking.objects.all()\
        .annotate(total_bookings=Count('employee')) \
        .order_by('-total_bookings')[:limit]

    return top_employees