from django.db import models

# Create your models here.


class ChickenDiseaseSample(models.Model):
    disease_name_predicted = models.CharField(max_length=100)
    disease_sample_picture = models.ImageField(upload_to='chicken_sample')
    conifidence_level = models.FloatField()