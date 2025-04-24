from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Create your views here.


MODEL_PATH = settings.BASE_DIR / 'ml_model' / 'chickenDiseaseDitectionVersion2.h5'
model = load_model(MODEL_PATH)

def taking_sample(request):
    if request.method == "POST":
        img = request.FILES['sample_image']
        img = image.load_img(img, target_size=(256,256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        # Making the prediction
        prediction = model.predict(img_array)
        predicted_result = np.argmax()
        
        
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")
