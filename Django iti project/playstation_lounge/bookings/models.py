from django.db import models
from django.core.validators import MinValueValidator
from facilities.models import Room, BilliardTable, MenuItem
from decimal import Decimal

class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=17)
    booking_date = models.DateTimeField()
    duration_hours = models.IntegerField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.pk} - {self.customer_name}"

    class Meta:
        ordering = ['-booking_date']

    def get_total_price(self):
        total = Decimal('0.00')
        
        # Add room costs
        for booking_room in self.bookingroom_set.all():
            total += booking_room.room.hourly_price * booking_room.hours
        
        # Add billiard costs
        for booking_billiard in self.bookingbilliard_set.all():
            total += booking_billiard.billiard_table.hourly_price * booking_billiard.hours
        
        # Add menu item costs
        for booking_menu in self.bookingmenuitem_set.all():
            total += booking_menu.menu_item.price * booking_menu.quantity
        
        return total

class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hours = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.room.name} for {self.hours} hours"

    def get_subtotal(self):
        return self.room.hourly_price * self.hours

class BookingBilliard(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    billiard_table = models.ForeignKey(BilliardTable, on_delete=models.CASCADE)
    hours = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.billiard_table.name} for {self.hours} hours"

    def get_subtotal(self):
        return self.billiard_table.hourly_price * self.hours

class BookingMenuItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"

    def get_subtotal(self):
        return self.menu_item.price * self.quantity