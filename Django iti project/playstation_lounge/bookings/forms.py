from django import forms
from .models import Booking, BookingRoom, BookingBilliard, BookingMenuItem
from facilities.models import Room, BilliardTable, MenuItem

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'phone', 'booking_date', 'duration_hours', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'booking_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'}),
        }

class BookingRoomForm(forms.ModelForm):
    class Meta:
        model = BookingRoom
        fields = ['room', 'hours']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class BookingBilliardForm(forms.ModelForm):
    class Meta:
        model = BookingBilliard
        fields = ['billiard_table', 'hours']
        widgets = {
            'billiard_table': forms.Select(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class BookingMenuItemForm(forms.ModelForm):
    class Meta:
        model = BookingMenuItem
        fields = ['menu_item', 'quantity']
        widgets = {
            'menu_item': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }