from django.contrib import admin
from .models import Room, Messages, Topic, DirectMessage, DirectMessageRoom

# Register your models here.

admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Topic)
admin.site.register(DirectMessageRoom)
admin.site.register(DirectMessage)