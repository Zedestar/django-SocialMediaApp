from django.urls import path
from . import views

# - Creating the urls here 

urlpatterns = [
    path("uploading_chicken_sample/", views.taking_sample, name="taking_chicken_sample"),
    path("showing_the_sample_results/", views.taking_sample, name="taking_chicken_sample"),
]
