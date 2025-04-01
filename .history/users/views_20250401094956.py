from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreateUserForm, ProfileForm
from .models import Profile

##############################################################################
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage

##############################################################################
from .tokens import account_activation_token
from .models import Profile

# Create your views here.


def activateEmail(request, user, to_email):
    mail_subject = "Activate your account."
    message = render_to_string(
        "users/activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(
            request,
            f"Dear {user.username} please go to your email inbo and click to your received \
            link to confirm the complete registration, NB: chack your spam email",
        )
    else:
        messages.error(
            request,
            f"Fail to send the email to {to_email}. Please type your email correctly",
        )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.success(request, f"{username} your successifully logged in")
                login(request, user)
            else:
                messages.error(request, "Invalid credentials")
        else:
            for key, error in list(form.errors.items()):
                if key == "captcha":
                    messages.error(request, "Pass the captcha field")
                else:
                    messages.error(request, error)
    else:
        form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, "users/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Your sucessfully logged out")
    return render(request, "users/logout.html")


def user_registration_view(request):
    if request.method == "POST":
        print(request.POST)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))

            # messages.success(request, f"{form.cleaned_data['username']} Your successfully registered")
            return redirect("login")
        else:
            for error in form.errors.values():
                messages.error(request, error)
                print(error)
    else:
        form = CreateUserForm()
    context = {
        "form": form,
    }
    return render(request, "users/user_registration_form.html", context)


def activate(request, uidb64, token):
    print("these are the uidb64 and token", uidb64, token)
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:  # and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Thank you for your email confirmation. You can now log in to your account.",
        )
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid.")
        print(f"Token valid: {account_activation_token.check_token(user, token)}")
        return render(request, "users/activation_invalid.html")


def already_signup_redirect(request):
    messages.error(
        request,
        "Something went wrong here. You might be already signed up, try to login it with same creditiacials as from google",
    )
    return redirect("login")


def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {"profile": profile}
    return render(request, "users/profile.html", context)


def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.photo = request.POST.get("photo")
            profile.save()
            messages.success(request, "Profile created successfully")
            return redirect("index")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ProfileForm()
    context = {
        "form": form,
    }
    return render(request, "users/create_profile.html", context)


def edit_profile(request, id):
    profile = Profile.objects.get(id=id)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile created successfully")
            return redirect("profile")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ProfileForm(instance=profile)
    context = {
        "form": form,
    }
    return render(request, "users/edit_profile.html", context)
