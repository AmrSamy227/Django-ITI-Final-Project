from django.shortcuts import render
from django.db.models import Sum, Count, F, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from bookings.models import Booking, BookingRoom, BookingBilliard, BookingMenuItem
from facilities.models import Room, BilliardTable, MenuItem
from customers.models import Customer
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone


def dashboard_home(request):
    date_filter = request.GET.get('filter', 'all')

    start_date = None
    end_date = timezone.now()

    if date_filter == 'today':
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_filter == 'week':
        start_date = timezone.now() - timedelta(days=7)
    elif date_filter == 'month':
        start_date = timezone.now() - timedelta(days=30)

    bookings_query = Booking.objects.all()
    if start_date:
        bookings_query = bookings_query.filter(booking_date__gte=start_date)

    room_hours_data = BookingRoom.objects.filter(
        booking__in=bookings_query
    ).values(
        'room__name'
    ).annotate(
        total_hours=Sum('hours')
    ).order_by('-total_hours')

    most_booked_rooms = BookingRoom.objects.filter(
        booking__in=bookings_query
    ).values(
        'room__name'
    ).annotate(
        booking_count=Count('id')
    ).order_by('-booking_count')[:5]

    billiard_hours_data = BookingBilliard.objects.filter(
        booking__in=bookings_query
    ).values(
        'billiard_table__name'
    ).annotate(
        total_hours=Sum('hours')
    ).order_by('-total_hours')

    most_used_billiards = BookingBilliard.objects.filter(
        booking__in=bookings_query
    ).values(
        'billiard_table__name'
    ).annotate(
        usage_count=Count('id')
    ).order_by('-usage_count')[:5]

    top_menu_items = BookingMenuItem.objects.filter(
        booking__in=bookings_query
    ).values(
        'menu_item__name'
    ).annotate(
        order_count=Sum('quantity')
    ).order_by('-order_count')[:5]

    gaming_revenue = BookingRoom.objects.filter(
        booking__in=bookings_query
    ).annotate(
        subtotal=F('hours') * F('room__hourly_price')
    ).aggregate(
        total=Coalesce(Sum('subtotal', output_field=DecimalField()), Decimal('0.00'))
    )['total']

    billiard_revenue = BookingBilliard.objects.filter(
        booking__in=bookings_query
    ).annotate(
        subtotal=F('hours') * F('billiard_table__hourly_price')
    ).aggregate(
        total=Coalesce(Sum('subtotal', output_field=DecimalField()), Decimal('0.00'))
    )['total']

    menu_revenue = BookingMenuItem.objects.filter(
        booking__in=bookings_query
    ).annotate(
        subtotal=F('quantity') * F('menu_item__price')
    ).aggregate(
        total=Coalesce(Sum('subtotal', output_field=DecimalField()), Decimal('0.00'))
    )['total']

    total_revenue = gaming_revenue + billiard_revenue + menu_revenue

    total_bookings = bookings_query.count()

    active_sessions = bookings_query.filter(
        booking_date__lte=timezone.now(),
        booking_date__gte=timezone.now() - timedelta(hours=24)
    ).count()

    total_customers = Customer.objects.count()

    top_customers = []
    for customer in Customer.objects.all()[:10]:
        customer_bookings = bookings_query.filter(
            customer_name=customer.name,
            phone=customer.phone
        ).count()
        if customer_bookings > 0:
            top_customers.append({
                'name': customer.name,
                'phone': customer.phone,
                'booking_count': customer_bookings
            })

    top_customers = sorted(top_customers, key=lambda x: x['booking_count'], reverse=True)[:10]

    context = {
        'total_revenue': total_revenue,
        'gaming_revenue': gaming_revenue,
        'billiard_revenue': billiard_revenue,
        'menu_revenue': menu_revenue,
        'total_bookings': total_bookings,
        'active_sessions': active_sessions,
        'total_customers': total_customers,
        'room_hours_data': list(room_hours_data),
        'most_booked_rooms': list(most_booked_rooms),
        'billiard_hours_data': list(billiard_hours_data),
        'most_used_billiards': list(most_used_billiards),
        'top_menu_items': list(top_menu_items),
        'top_customers': top_customers,
        'date_filter': date_filter,
    }

    return render(request, 'dashboard/dashboard.html', context)
