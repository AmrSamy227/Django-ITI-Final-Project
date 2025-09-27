from django.contrib import admin
from .models import Booking, BookingRoom, BookingBilliard, BookingMenuItem

class BookingRoomInline(admin.TabularInline):
    model = BookingRoom
    extra = 0

class BookingBilliardInline(admin.TabularInline):
    model = BookingBilliard
    extra = 0

class BookingMenuItemInline(admin.TabularInline):
    model = BookingMenuItem
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer_name', 'phone', 'booking_date', 'duration_hours', 'get_total_price')
    list_filter = ('booking_date', 'created_at')
    search_fields = ('customer_name', 'phone')
    inlines = [BookingRoomInline, BookingBilliardInline, BookingMenuItemInline]
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'