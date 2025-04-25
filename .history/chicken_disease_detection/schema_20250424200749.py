import graphene
from graphene_file_upload.scalars import Upload
from tensoflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from io import BytesIO
from django.conf import settings


