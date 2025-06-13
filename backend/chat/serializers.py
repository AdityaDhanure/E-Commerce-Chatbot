from rest_framework import serializers
from .models import ChatSession, ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__' # Include all fields from the model
        read_only_fields = ['session', 'sender', 'timestamp'] # These fields are set by the backend

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    # Display the username for read operations, but don't expect it on input
    username = serializers.CharField(source='user.username', read_only=True, allow_null=True)

    class Meta:
        model = ChatSession
        # Expose the 'id' (which is now the UUID), 'user' (for internal use, not for direct setting by client), and other fields
        fields = ['id', 'user', 'username', 'created_at', 'updated_at', 'is_active', 'messages']
        # 'user' is read-only here because the view will set it based on request.user
        read_only_fields = ['id', 'user', 'username', 'created_at', 'updated_at', 'is_active', 'messages']