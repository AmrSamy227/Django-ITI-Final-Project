from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Booking, BookingRoom, BookingBilliard, BookingMenuItem
from .forms import BookingForm, BookingRoomForm, BookingBilliardForm, BookingMenuItemForm
from facilities.models import Room, BilliardTable, MenuItem

def booking_list(request):
    search_query = request.GET.get('search', '')
    bookings = Booking.objects.all()
    
    if search_query:
        bookings = bookings.filter(
            Q(customer_name__icontains=search_query) | 
            Q(phone__icontains=search_query)
        )
    
    context = {
        'bookings': bookings,
        'search_query': search_query,
    }
    return render(request, 'bookings/booking_list.html', context)

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking_rooms = BookingRoom.objects.filter(booking=booking)
    booking_billiards = BookingBilliard.objects.filter(booking=booking)
    booking_menu_items = BookingMenuItem.objects.filter(booking=booking)
    
    context = {
        'booking': booking,
        'booking_rooms': booking_rooms,
        'booking_billiards': booking_billiards,
        'booking_menu_items': booking_menu_items,
    }
    return render(request, 'bookings/booking_detail.html', context)

def booking_create_step1(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, 'Booking created! Now add facilities and items.')
            return redirect('bookings:booking_create_step2', booking_id=booking.pk)
    else:
        form = BookingForm()
    
    return render(request, 'bookings/booking_step1.html', {'form': form})

def booking_create_step2(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking_rooms = BookingRoom.objects.filter(booking=booking)
    booking_billiards = BookingBilliard.objects.filter(booking=booking)
    booking_menu_items = BookingMenuItem.objects.filter(booking=booking)
    
    rooms = Room.objects.all()
    billiards = BilliardTable.objects.all()
    menu_items = MenuItem.objects.all()
    
    context = {
        'booking': booking,
        'booking_rooms': booking_rooms,
        'booking_billiards': booking_billiards,
        'booking_menu_items': booking_menu_items,
        'rooms': rooms,
        'billiards': billiards,
        'menu_items': menu_items,
    }
    return render(request, 'bookings/booking_step2.html', context)

def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'bookings/booking_form.html', {'form': form, 'title': 'Update Booking'})

def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
        return redirect('bookings:booking_list')
    
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})

def add_booking_room(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        form = BookingRoomForm(request.POST)
        if form.is_valid():
            booking_room = form.save(commit=False)
            booking_room.booking = booking
            booking_room.save()
            messages.success(request, 'Room added to booking!')
            return redirect('bookings:booking_create_step2', booking_id=booking.pk)
    
    return redirect('bookings:booking_create_step2', booking_id=booking.pk)

def add_booking_billiard(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        form = BookingBilliardForm(request.POST)
        if form.is_valid():
            booking_billiard = form.save(commit=False)
            booking_billiard.booking = booking
            booking_billiard.save()
            messages.success(request, 'Billiard table added to booking!')
            return redirect('bookings:booking_create_step2', booking_id=booking.pk)
    
    return redirect('bookings:booking_create_step2', booking_id=booking.pk)

def add_booking_menu(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        form = BookingMenuItemForm(request.POST)
        if form.is_valid():
            booking_menu = form.save(commit=False)
            booking_menu.booking = booking
            booking_menu.save()
            messages.success(request, 'Menu item added to booking!')
            return redirect('bookings:booking_create_step2', booking_id=booking.pk)
    
    return redirect('bookings:booking_create_step2', booking_id=booking.pk)

def delete_booking_room(request, pk):
    booking_room = get_object_or_404(BookingRoom, pk=pk)
    booking_id = booking_room.booking.pk
    booking_room.delete()
    messages.success(request, 'Room removed from booking!')
    return redirect('bookings:booking_create_step2', booking_id=booking_id)

def delete_booking_billiard(request, pk):
    booking_billiard = get_object_or_404(BookingBilliard, pk=pk)
    booking_id = booking_billiard.booking.pk
    booking_billiard.delete()
    messages.success(request, 'Billiard table removed from booking!')
    return redirect('bookings:booking_create_step2', booking_id=booking_id)

def delete_booking_menu(request, pk):
    booking_menu = get_object_or_404(BookingMenuItem, pk=pk)
    booking_id = booking_menu.booking.pk
    booking_menu.delete()
    messages.success(request, 'Menu item removed from booking!')
    return redirect('bookings:booking_create_step2', booking_id=booking_id)