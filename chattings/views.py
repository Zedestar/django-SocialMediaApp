from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'chattings/home.html')



def room(request, pk):
    return render(request, 'chattings/room.html')
