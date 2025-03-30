from .models import Room
from django import forms

# - Creating the forms here 


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        