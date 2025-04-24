from django.shortcuts import render
from tensorflow.keras.models

# Create your views here.


def taking_sample(request):
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")
