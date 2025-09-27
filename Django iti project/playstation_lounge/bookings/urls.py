from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/', views.booking_create_step1, name='booking_create_step1'),
    path('create/step2/<int:booking_id>/', views.booking_create_step2, name='booking_create_step2'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('<int:pk>/update/', views.booking_update, name='booking_update'),
    path('<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('<int:booking_id>/add-room/', views.add_booking_room, name='add_booking_room'),
    path('<int:booking_id>/add-billiard/', views.add_booking_billiard, name='add_booking_billiard'),
    path('<int:booking_id>/add-menu/', views.add_booking_menu, name='add_booking_menu'),
    path('room/<int:pk>/delete/', views.delete_booking_room, name='delete_booking_room'),
    path('billiard/<int:pk>/delete/', views.delete_booking_billiard, name='delete_booking_billiard'),
    path('menu/<int:pk>/delete/', views.delete_booking_menu, name='delete_booking_menu'),
]