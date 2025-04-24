from django.urls import path
from . import views

# - Creating the urls here 

urlpatterns = [
    path("uploading_chicken_sample/", views.taking_sample, name="taking_chicken_sample"),
]
