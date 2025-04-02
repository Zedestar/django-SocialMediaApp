from django.contrib.auth.models import User
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your username",
                "class": "p-1 rounded-sm",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "class": "p-1 rounded-sm",
            }
        ),
        required=True,
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "p-1 rounded-sm "}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Re enter your password", "class": "p-1 rounded-sm"}
        ),
    )
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username", "class": "p-1 rounded-sm"}
        ),
    )

    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "class": "p-1 rounded-sm "}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two passwords does not match")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f"the email {email} already exists, try another email"
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f"The username {username} already exists, try other one"
            )
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
