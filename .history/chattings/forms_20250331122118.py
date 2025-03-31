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
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 2,  # Ensures the textarea is 2 rows tall
                "class": "p-2 rounded-md border border-gray-300 w-full resize-none",  # Tailwind styles
                "placeholder": "Type your message...",
            })
        }
