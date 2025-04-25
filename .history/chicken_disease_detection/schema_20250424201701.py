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

class PredictedDisease(graphene.Mutation):
    class Arguments:
        sample_image = Upload(required=True)
        
    prediction = graphene.String()
    
    def mutate
