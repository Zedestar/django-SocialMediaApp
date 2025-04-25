import graphene
from graphene_file_upload.scalars import Upload
from tensoflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from io import BytesIO
from django.conf import settings

# Loading the model
MODEL_PATH = settings.BASE_DIR / 'ml_model' / 'chickenDiseaseDitectionVersion1.h5'
model = load_model(MODEL_PATH)
class_labels = ['COCCIDIOSIS', 'HEALTH', 'NEWCASTLEDISEASE', 'SALMONELLA']

class PredictDisease(graphene.Mutation):
    class Arguments:
        sample_image = Upload(required=True)
        
    prediction = graphene.String()
    
    def mutate(self, info, sample_image):
         # Read image from Upload and convert to PIL
        img = image.load_img(BytesIO(sample_image.read()), target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction, axis=1)[0]
        predicted_label = class_labels[predicted_index]

        return PredictDisease(prediction=predicted_label)
    
class Mutation
