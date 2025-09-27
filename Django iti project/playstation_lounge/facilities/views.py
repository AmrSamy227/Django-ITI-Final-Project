from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room, BilliardTable, MenuItem
from .forms import RoomForm, BilliardTableForm, MenuItemForm

# Room Views
def room_list(request):
    search_query = request.GET.get('search', '')
    rooms = Room.objects.all()
    
    if search_query:
        rooms = rooms.filter(
            Q(name__icontains=search_query) | 
            Q(console__icontains=search_query)
        )
    
    context = {
        'rooms': rooms,
        'search_query': search_query,
    }
    return render(request, 'facilities/room_list.html', context)

def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully!')
            return redirect('facilities:room_list')
    else:
        form = RoomForm()
    
    return render(request, 'facilities/room_form.html', {'form': form, 'title': 'Create Room'})

def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('facilities:room_list')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'facilities/room_form.html', {'form': form, 'title': 'Update Room'})

def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully!')
        return redirect('facilities:room_list')
    
    return render(request, 'facilities/room_confirm_delete.html', {'room': room})

# Billiard Table Views
def billiard_list(request):
    search_query = request.GET.get('search', '')
    billiards = BilliardTable.objects.all()
    
    if search_query:
        billiards = billiards.filter(name__icontains=search_query)
    
    context = {
        'billiards': billiards,
        'search_query': search_query,
    }
    return render(request, 'facilities/billiard_list.html', context)

def billiard_create(request):
    if request.method == 'POST':
        form = BilliardTableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billiard table created successfully!')
            return redirect('facilities:billiard_list')
    else:
        form = BilliardTableForm()
    
    return render(request, 'facilities/billiard_form.html', {'form': form, 'title': 'Create Billiard Table'})

def billiard_update(request, pk):
    billiard = get_object_or_404(BilliardTable, pk=pk)
    if request.method == 'POST':
        form = BilliardTableForm(request.POST, instance=billiard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billiard table updated successfully!')
            return redirect('facilities:billiard_list')
    else:
        form = BilliardTableForm(instance=billiard)
    
    return render(request, 'facilities/billiard_form.html', {'form': form, 'title': 'Update Billiard Table'})

def billiard_delete(request, pk):
    billiard = get_object_or_404(BilliardTable, pk=pk)
    if request.method == 'POST':
        billiard.delete()
        messages.success(request, 'Billiard table deleted successfully!')
        return redirect('facilities:billiard_list')
    
    return render(request, 'facilities/billiard_confirm_delete.html', {'billiard': billiard})

# Menu Item Views
def menu_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    menu_items = MenuItem.objects.all()
    
    if search_query:
        menu_items = menu_items.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        menu_items = menu_items.filter(category=category_filter)
    
    categories = MenuItem.CATEGORY_CHOICES
    
    context = {
        'menu_items': menu_items,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    return render(request, 'facilities/menu_list.html', context)

def menu_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item created successfully!')
            return redirect('facilities:menu_list')
    else:
        form = MenuItemForm()
    
    return render(request, 'facilities/menu_form.html', {'form': form, 'title': 'Create Menu Item'})

def menu_update(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('facilities:menu_list')
    else:
        form = MenuItemForm(instance=menu_item)
    
    return render(request, 'facilities/menu_form.html', {'form': form, 'title': 'Update Menu Item'})

def menu_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        menu_item.delete()
        messages.success(request, 'Menu item deleted successfully!')
        return redirect('facilities:menu_list')
    
    return render(request, 'facilities/menu_confirm_delete.html', {'menu_item': menu_item})