from django.shortcuts import render, get_object_or_404
from .models import Room, Topic, Messages, DirectMessageRoom, DirectMessage
from .forms import RoomForm, MessageForm, DirectMessageForm
from users.models import Profile
from django.contrib.auth import get_user_model
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
        recent_messages_activity = Messages.objects.filter(room__in=rooms).order_by("-created_at")[:15]
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms, 
        'topics': topics, 
        'search':room_search_Query, 
        'room_count': room_count,
        'recent_messages_activity': recent_messages_activity,
        }
    return render(request, 'chattings/home.html', context=context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.room_messages.all()
    if request.method == "POST":
        form = MessageForm(request.POST)
        form_type = request.POST.get('form_type')
        if form_type == 'message_form':
            if request.user not in room.participants.all():
                messages.warning(request, f"Join to {room.name} room to send messages")
                return redirect("chattings_room", room.id)
            else:
                if form.is_valid():
                    message = form.save(commit=False)
                    message.room = room 
                    message.sender = request.user
                    message.save()
                    messages.success(request, "message created successfully")
                    return redirect("chattings_room", room.id)
                else:
                    for error in form.errors.values():
                        messages.error(request, f"{error}")
        elif form_type == 'delete_form':
            message_to_delete_id = request.POST.get('message_id')
            if message_to_delete_id:
                message_to_delete = get_object_or_404(Messages, id=message_to_delete_id)
                if request.user == message_to_delete.sender:
                    messages.success(request, f'message "{message_to_delete.content[0:10]}" deleted successfully')
                    message_to_delete.delete()
                    return redirect("chattings_room", room.id)
                else:
                    messages.error(request, "You are not allowed to delete this message")
        elif form_type == "join_form":
            room.participants.add(request.user)
            messages.success(request, f"You joined {room.name} successfully")
            return redirect("chattings_room", room.id)
        elif form_type == "leave_form":
            room.participants.remove(request.user)
            messages.success(request, f"You left {room.name} successfully")
            return redirect("chattings_room", room.id)
    else:
        form = MessageForm()
    context = {
        "room":room,
        "room_messages": room_messages,
        "room_owner": room.host.username,
        "form":form,
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

@login_required
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





def user_profile(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        sender = request.user
        receiva  = user

        # Check if a chat room exists in both directions
        inbox_room = DirectMessageRoom.objects.filter(
            sender=sender, reciver=receiva
        ).first() or DirectMessageRoom.objects.filter(
            sender=receiva, reciver=sender
        ).first()

        # If no room exists, create one
        if not inbox_room:
            inbox_room = DirectMessageRoom.objects.create(sender=sender, reciver=receiva)

        return redirect("inbox_room", inbox_room.id)

    context = {
        "user_profile": user_profile,
        "user": user,
    }
    return render(request, "chattings/userdataProfile.html", context)


def the_inbox_room(request, pk):
    inbox_room = DirectMessageRoom.objects.get(id=pk)
    inbox_messages = DirectMessage.objects.filter(room=inbox_room).order_by(F("created_at").desc())
    my_charts_room = DirectMessageRoom.objects.filter(
        Q(sender=request.user) | 
        Q(reciver=request.user)
    )
    chat_partners = [
    room.reciver if room.sender == request.user else room.sender
    for room in my_charts_room
    ]
    
    if request.method == "POST":
        form = DirectMessageForm(request.POST)
        form_type = request.POST.get('form_type')
        if form_type == 'message_form':
                if form.is_valid():
                    message = form.save(commit=False)
                    message.room = inbox_room 
                    message.sender = request.user
                    message.save()
                    messages.success(request, "message sent successfully")
                    return redirect("inbox_room", inbox_room.id)
                else:
                    for error in form.errors.values():
                        messages.error(request, f"{error}")
        elif form_type == 'delete_form':
            message_to_delete_id = request.POST.get('message_id')
            if message_to_delete_id:
                message_to_delete = get_object_or_404(DirectMessage, id=message_to_delete_id)
                if request.user == message_to_delete.sender:
                    messages.success(request, f'message "{message_to_delete.content[0:10]}" deleted successfully')
                    message_to_delete.delete()
                    return redirect("inbox_room", inbox_room.id)
                else:
                    messages.error(request, "You are not allowed to delete this message")
    else:
        form = DirectMessageForm()
    context = {
        "inbox_room": inbox_room,
        "inbox_messages": inbox_messages,
        "form": form,
        "chart_partners": chat_partners
    }
    return render(request, 'chattings/inbox_room.html', context)