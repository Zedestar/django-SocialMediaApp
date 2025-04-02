from django.urls import path
from . import views

# - The urls patterns

urlpatterns = [
    path("", views.index, name="index"),
    path("post_item/<slug:slug>/", views.post_item, name="post_item"),
    path("create_post/", views.create_post, name="create_post"),
    path("like_post/", views.like_post, name="like_post"),
    path("dislike_post/", views.dislike_post, name="dislike_post"),
    path("bookmark_post/", views.bookmark_post, name="bookmark_post"),
]
