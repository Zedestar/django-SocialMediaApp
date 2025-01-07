from django.contrib import admin
from .models import Post, Comment, Replay, ReplayToReplay

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Replay)
admin.site.register(ReplayToReplay)
