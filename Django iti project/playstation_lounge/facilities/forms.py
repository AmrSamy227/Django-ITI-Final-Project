from django import forms
from .models import Room, BilliardTable, MenuItem

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'console', 'hourly_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Room 1'}),
            'console': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., PS5'}),
            'hourly_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

class BilliardTableForm(forms.ModelForm):
    class Meta:
        model = BilliardTable
        fields = ['name', 'hourly_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Table 1'}),
            'hourly_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }