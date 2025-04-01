from django.db import models
from django.conf import settings

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hosted_rooms", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, related_name="room_topics", on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="room_participants", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return self.name



class Messages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, related_name="room_messages", on_delete=models.PROTECT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sender.username} - {self.room.name} - {self.content[0:10]}"
    
    
    
class DirectMessageRoom(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sender_messages", on_delete=models.CASCADE)
    reciver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reciver_messages", on_delete=models.CASCADE)
    