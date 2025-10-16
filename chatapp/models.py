import hashlib
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # ✅ Needed for the Room.owner relation


class ChatMessage(models.Model):
    username = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    message_hash = models.CharField(max_length=64, blank=True)
    previous_hash = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last = ChatMessage.objects.filter(room_name=self.room_name).order_by('-timestamp').first()
            self.previous_hash = last.message_hash if last else '0' * 64

            data = (
                self.username +
                self.room_name +
                self.message +
                str(self.timestamp) +
                self.previous_hash
            ).encode()

            self.message_hash = hashlib.sha256(data).hexdigest()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}: {self.message[:30]}"


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_pin = models.CharField(max_length=128, null=True, blank=True)  # Hashed PIN
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_rooms", null=True, blank=True)  # ✅ Added field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pin = None

    def set_pin(self, raw_pin):
        """Hash and store the room PIN."""
        self.room_pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        """Verify the raw PIN against the hashed value."""
        return check_password(raw_pin, self.room_pin)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()
    message_hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in {self.room.room_name}: {self.message[:30]}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    pin = models.CharField(max_length=128)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.room.room_name}"

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    message_hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}: {self.message[:30]}"
