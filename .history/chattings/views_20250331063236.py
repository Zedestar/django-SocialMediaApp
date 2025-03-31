from django.shortcuts import render
from .models import Room, Topic
from .forms import RoomForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import F, Q, Count
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    if request.method == 'GET':
        room_filter_query = request.GET.get('q')
        room_search_Query = request.GET.get('search')
        if room_search_Query:
            rooms = Room.objects.filter(
                Q(topic__name__icontains = room_search_Query) |
                Q(name__icontains = room_search_Query) | 
                Q(description__icontains = room_search_Query) | 
                Q(host__username__icontains = room_search_Query)
                )
        elif room_filter_query:
            rooms = Room.objects.filter(topic__name__icontains = room_filter_query)
        else:
            rooms = Room.objects.all()
       
        
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms, 
        'topics': topics, 
        'search':room_search_Query, 
        'room_count': room_count
        }
    return render(request, 'chattings/home.html', context=context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        "room":room
    }
    return render(request, 'chattings/room.html', context=context)

@login_required
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
    context = {
        'form': form
        }
    return render(request, 'chattings/create_room_form.html', context=context)


@login_required
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, 'You are not allowed to update this room')
        return redirect('chattings_home')
    else:    
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
    context = {
        'form': form
        }
    return render(request, 'chattings/update_room_form.html', context=context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user!= room.host:
        messages.error(request, 'You are not allowed to delete this room')
        return redirect('chattings_home')
    else:
        if request.method == "POST":
            room.delete()
            messages.success(request, "Room deleted SUccessfully")
            return redirect("chattings_home")
    context = {
        "room": room,
    }
    return render(request, "chattings/delete_room_form.html", context=context)