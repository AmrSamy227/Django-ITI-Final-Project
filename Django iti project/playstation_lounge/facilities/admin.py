from django.contrib import admin
from .models import Room, BilliardTable, MenuItem

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'console', 'hourly_price', 'created_at')
    list_filter = ('console', 'created_at')
    search_fields = ('name', 'console')

@admin.register(BilliardTable)
class BilliardTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'hourly_price', 'created_at')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')