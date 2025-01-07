import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="my_posts",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(upload_to="photo_posts", blank=False, null=False)
    title = models.CharField(max_length=200, blank=False, null=False)
    caption = models.TextField()
    slug = models.SlugField(max_length=200, null=True, blank=True)
    viewers = models.IntegerField(default=0)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="posts_liked", blank=True
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="posts_disliked", blank=True
    )
    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="post_bookmarked", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1
        # Check if a post with the same slug exists
        while Post.objects.filter(slug=unique_slug).exists():
            # Append counter to make it unique
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post.title} {self.user.username}"
    

class Replay(models.Model):
    comment = models.ForeignKey(Comment, related_name="replays", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="replays", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="replays", on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.comment} {self.post} {self.user.username}"
    
    
class ReplayToReplay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    parent_replay = models.ForeignKey(Replay, related_name="nested_replies", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nested_replies_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="nested_replies_receiver", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"This is from {self.sender.username} to {self.receiver.username}"
    
    
    
    
    
    
    
    
