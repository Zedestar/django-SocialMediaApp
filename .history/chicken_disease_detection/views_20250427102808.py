from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from io import BytesIO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.shortcuts import get_object_or_404
import numpy as np
from PIL import Image
from .models import ChickenDiseaseSample

# Create your views here.


MODEL_PATH = settings.BASE_DIR / 'ml_model' / 'chickenDiseaseDitectionVersion1.h5'
model = load_model(MODEL_PATH)
class_labels = ['COCCIDIOSIS', 'HEALTH', 'NEWCASTLEDISEASE', 'SALMONELLA']

def taking_sample(request):
    if request.method == "POST":
        uploaded_file = request.FILES['sample_image']
        if uploaded_file:
            img = image.load_img(BytesIO(uploaded_file.read()), target_size=(224,224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            # Making the prediction
            prediction = model.predict(img_array)
            predicted_result = np.argmax(prediction, axis=1)
            confidence_level = prediction[0][predicted_result]
            predicted_label = class_labels[predicted_result[0]]
            sample = ChickenDiseaseSample.objects.create(
                user = request.user,
                disease_name_predicted = predicted_label,
                disease_sample_picture = uploaded_file,
                confidence_level = confidence_level
            )
            print(f"The predicted data is {predicted_label}")
            print(f"The predicted data is {confidence_level}")
            
           
        return redirect(reverse("sample_result", args=[sample.id]))
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")


def sample_result(request, sample_id):
    sample_result = get_object_or_404(ChickenDiseaseSample, id=sample_id)
    context = {
                "prediction_label" : sample_result.disease_name_predicted,
                "confidence_level" : sample_result.confidence_level,
                "sample_picture" : sample_result.disease_sample_picture
            }
    return render(request, "chicken_disease_detection/show_sample_result.html")
