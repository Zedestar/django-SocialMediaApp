from django.urls import path
from . import views
from django.contrib.auth import views as authenticate_view

# - Setting the urls here

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "change_password/",
        authenticate_view.PasswordChangeView.as_view(
            template_name="users/change_password.html"
        ),
        name="change_password",
    ),
    path(
        "password_change_done/",
        authenticate_view.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "reset_password/",
        authenticate_view.PasswordResetView.as_view(
            template_name="users/reset_password.html"
        ),
        name="reset_password",
    ),
    path(
        "password_reset_done/",
        authenticate_view.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        authenticate_view.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        authenticate_view.PasswordResetCompleteView.as_view(
            template_name="users/password_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register_account/", views.user_registration_view, name="register_account"),
    path("activate/<uidb64>/token/<token>/", views.activate, name="activate"),
    path(
        "http://127.0.0.1:8000/accounts/3rdparty/signup/",
        views.already_signup_redirect,
        name="signup_redirect",
    ),
    path("profile/<str:pk>/", views.profile, name="profile"),
    path("create_profile/", views.create_profile, name="create_profile"),
    path("edit_profile/<int:id>/", views.edit_profile, name="edit_profile"),
]
