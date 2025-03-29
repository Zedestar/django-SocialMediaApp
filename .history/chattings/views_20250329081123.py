from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'chatting/home.html')



def room(request, pk):
    return render(request, 'chatting/room.html')
