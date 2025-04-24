from django.shortcuts import render

# Create your views here.


def taking_sample(request):
    return render(request, "chicken_disease_detection")
