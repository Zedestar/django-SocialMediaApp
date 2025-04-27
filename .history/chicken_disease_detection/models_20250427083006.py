from django.db import models
from django.conf import settings

# Create your models here.


class ChickenDiseaseSample(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    disease_name_predicted = models.CharField(max_length=100)
    disease_sample_picture = models.ImageField(upload_to='chicken_sample')
    conifidence_level = models.FloatField()
    time_taken = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"The disease {self.disease_name_predicted} confidence of {self.conifidence_level}"