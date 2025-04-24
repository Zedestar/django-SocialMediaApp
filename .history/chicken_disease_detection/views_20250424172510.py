from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model

# Create your views here.


MODEL_PATH = settings.BASE_DIR / 'ml_model' / 'chickenDiseaseDitectionVersion2.h5'
model = load_model(MODEL_PATH)

def taking_sample(request):
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")
