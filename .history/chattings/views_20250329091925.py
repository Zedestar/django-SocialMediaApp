from django.shortcuts import render
from .models import Room

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'chattings/home.html', context=context)



def room(request, pk):
    return render(request, 'chattings/room.html')
