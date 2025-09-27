from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    # Room URLs
    path('', views.room_list, name='room_list'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/update/', views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    
    # Billiard Table URLs
    path('billiards/', views.billiard_list, name='billiard_list'),
    path('billiards/create/', views.billiard_create, name='billiard_create'),
    path('billiards/<int:pk>/update/', views.billiard_update, name='billiard_update'),
    path('billiards/<int:pk>/delete/', views.billiard_delete, name='billiard_delete'),
    
    # Menu Item URLs
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/create/', views.menu_create, name='menu_create'),
    path('menu/<int:pk>/update/', views.menu_update, name='menu_update'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),
]