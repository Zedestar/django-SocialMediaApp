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
    form = RoomForm()
    context = {'form': form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully')
        else:
            for error in replay_form.errors.values():
                messages.error(request, error)
            return redirect('chattings_home')
    return render(request, 'chattings/create_room_form.html')

