from django.shortcuts import render
from django.conf import settings
from io import BytesIO
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Create your views here.


MODEL_PATH = settings.BASE_DIR / 'ml_model' / 'chickenDiseaseDitectionVersion2.h5'
model = load_model(MODEL_PATH)
class_labels = ['COCCIDIOSIS', 'HEALTH', 'NEWCASTLEDISEASE', 'SALMONELLA']

def taking_sample(request):
    if request.method == "POST":
        # uploaded_file = request.FILES['sample_image']
        # img = image.load_img(BytesIO(uploaded_file.read()), target_size=(224,224))
        # img_array = image.img_to_array(img) / 255.0
        # img_array = np.expand_dims(img_array, axis=0)
        # # Making the prediction
        # prediction = model.predict(img_array)
        # # predicted_result = np.argmax(prediction, axis=1)
        # print(f"The predicted data is {prediction}")
        image = request.FILES['sample_image']
        # Preprocessing the image
        img = Image.open(image)
        img = img.resize((224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array= np.expand_dims(img_array, axis=0)
        
        # Making predctions
        predictions = model.predict(img_array)
        predicted_label = class_labels[np.argmax(predictions)]
        print(f"THE PREDICTED LABEL IS {predicted_label}")
        
        
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")
