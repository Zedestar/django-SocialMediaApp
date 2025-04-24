from django.shortcuts import render
from tensorflow.keras.models import load_model

# Create your views here.


MODEL_PATH = BASE_DIR / 'ml_model' / ''

def taking_sample(request):
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")
