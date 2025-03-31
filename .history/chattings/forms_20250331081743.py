from django import forms
from .models import Room, Messages

# - Creating the forms here 


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ["content"]