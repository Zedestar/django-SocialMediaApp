from django.shortcuts import render, redirect
from .models import Post, Comment, Replay
from .forms import PostForm, CommentForm, ReplayForm
from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    posts = Post.objects.all().order_by("?")
    context = {
        "posts": posts,
    }
    return render(request, "posts/index.html", context)


def post_item(request, slug):
    comment_form = CommentForm()
    replay_form = ReplayForm()
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_id = request.POST.get('comment_id')
        if post_id and comment_id == None:
            post = Post.objects.get(id=post_id)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
            else:
                for error in comment_form.errors.values():
                    messages.error(request, error)
        elif post_id and comment_id:
            
            comment = get_object_or_404(Comment, id=comment_id)
            post = get_object_or_404(Post, id=post_id)
            replay_form = ReplayForm(request.POST)
            if replay_form.is_valid():
                replay = replay_form.save(commit=False)
                replay.comment = comment
                replay.user = request.user
                replay.post = post
                replay.save()
            else:
                for error in replay_form.errors.values():
                    messages.error(request, error)
        else:
            print("The obejct is neither comment of replay")
        
        
    # - Retrieving the comment selected by the user
    post_item = Post.objects.get(slug=slug)
    post_item.viewers = F("viewers") + 1
    post_item.save()
    post_item.refresh_from_db()

    # - Checking the comments related to the post_item
    comments = Comment.objects.filter(post=post_item)
    
    # - Checking the replays related to the comment selected
    context = {
        "post_item": post_item,
        "comments": comments,
        "comment_form": comment_form,
        "replay_form": replay_form,
        }
    return render(request, "posts/post_item.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(
                request,
                f"The post with title {request.POST.get('title')} was successfully saved",
            )
            return redirect("index")
    else:
        form = PostForm()
    context = {
        "form": form,
    }
    return render(request, "posts/create_post.html", context)


@login_required
def like_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
    return redirect("post_item", post.slug)


@login_required
def dislike_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
    return redirect("post_item", post.slug)


@login_required
def bookmark_post(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    if post.bookmark.filter(id=request.user.id).exists():
        post.bookmark.remove(request.user)
    else:
        post.bookmark.add(request.user)
    return redirect("post_item", post.slug)


###### TODO
# Creating functionality for view my bookmarked post and likes and well as disliked posts
