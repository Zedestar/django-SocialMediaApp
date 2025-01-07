from django import forms
from .models import *

# Creating forms


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        label="Post title",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter post title", "class": "p-1 rounded-sm"}
        ),
    )

    caption = forms.Textarea(
        # "placeholder":"Enter post caption"
    )

    photo = forms.ImageField(required=True, label="Post photo")

    class Meta:
        model = Post
        fields = ["title", "caption", "photo"]


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        label = "Your comment",
        max_length=1000,
        widget= forms.Textarea(
            attrs={
                "placeholder":"Write your comment",
                "rows":"2",
            }
        )
    )
    
    class Meta:
        model = Comment
        fields = ["body"]
        
        
        
class ReplayForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        label = "Your replay",
        max_length=1000,
        widget= forms.Textarea(
            attrs={
                "placeholder":"Write your replay",
                "rows":"2",
            }
        )
    )
    
    class Meta:
        model = Replay
        fields = ["body"]