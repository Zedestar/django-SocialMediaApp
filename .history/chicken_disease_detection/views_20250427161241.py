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
            print(f"The predicted data is {prediction}")
            
           
        return redirect(reverse("sample_result", args=[sample.id]))
    return render(request, "chicken_disease_detection/uploading_chicken_sample.html")


def sample_result(request, sample_id):
    sample_result = get_object_or_404(ChickenDiseaseSample, id=sample_id)
    disease_name = sample_result.disease_name_predicted
    confidence = sample_result.confidence_level
    picture = sample_result.disease_sample_picture
    context = {
                "prediction_label" : disease_name,
                "confidence_level" : confidence,
                "sample_picture" : picture
            }
    return render(request, "chicken_disease_detection/show_sample_result.html", context=context)

def my_samples(request):
    current_user = request.user
    sample_results = ChickenDiseaseSample.objects.filter(user=current_user)
    context = {
        "samples":sample_results
    }
    return render(request, "chicken_disease_detection/my_samples.html", context=context)



class PredictDiseaseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        sample_image = request.FILES.get('sample_image')

        if not sample_image:
            return Response({"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Read and prepare image
        img = image.load_img(BytesIO(sample_image.read()), target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction, axis=1)[0]
        predicted_label = class_labels[predicted_index]
        confidence_level = float(prediction[0][predicted_index])

        # Save the sample into the database
        sample = ChickenDiseaseSample.objects.create(
            user=request.user if request.user.is_authenticated else None,
            disease_name_predicted=predicted_label,
            disease_sample_picture=sample_image,  # Save the uploaded file
            confidence_level=confidence_level
        )

        # Return the result
        return Response({
            "id": sample.id,  # you can even return id if Flutter wants to navigate to sample detail page
            "prediction": predicted_label,
            "confidence_level": confidence_level,
            "time_taken": sample.time_taken
        }, status=status.HTTP_201_CREATED)