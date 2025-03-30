from django.shortcuts import render
from .models import Room
from .forms import RoomForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import F

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'chattings/home.html', context=context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        "room":room
    }
    return render(request, 'chattings/room.html', context=context)


def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully')
            return redirect('chattings_home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'chattings/create_room_form.html', context=context)



def update_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully')
            return redirect('chattings_home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'chattings/update_room_form.html', context=context)


def delete_room(request, pk):
    
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        messages.success(request, "Room deleted SUccessfully")
        return redirect("chattings_home")
    context = {
        
    }
    return render(request, "chattings/delete_room_form.html", context=context)