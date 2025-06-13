from django.db import models
from django.contrib.auth import get_user_model # Importing Django's get_user_model to support custom user models
import uuid # Importing uuid for generating unique session IDs

User = get_user_model() # Get the user model, which allows for custom user models in Django projects

class ChatSession(models.Model):
    # Changed primary_key to UUIDField for robustness, and made it the session ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Link to the User model.
    # null=True, blank=True allows for anonymous sessions (user field will be None).
    # on_delete=models.SET_NULL means if the User is deleted, their chat sessions remain but the 'user' field becomes NULL.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) # Indicates if the session is currently active

    def __str__(self):
        # Display username if user is linked, otherwise 'Anonymous'
        return f"Session {self.id} (User: {self.user.username if self.user else 'Anonymous'})"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50) # 'user' or 'chatbot'
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Stores product data returned by the chatbot, allowing flexible structure.
    products = models.JSONField(blank=True, null=True, default=list)

    class Meta:
        ordering = ['timestamp'] # Ensure messages are ordered chronologically

    def __str__(self):
        return f"{self.sender} in {self.session.id}: {self.message_text[:50]}"