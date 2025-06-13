from django.contrib import admin
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    # This allows you to see messages directly within the ChatSession admin page
    model = ChatMessage
    extra = 0 # Don't show empty extra forms
    readonly_fields = ['sender', 'message_text', 'timestamp', 'products'] # Messages should not be edited in admin
    can_delete = False # Prevent accidental deletion of messages via session
    show_change_link = True # Allow clicking to message details if needed

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    # Use the new fields from the ChatSession model
    list_display = (
        'id', # This is now the UUID for the session
        'user_display', # Custom method to display user info gracefully
        'created_at',
        'is_active',
        'message_count', # Custom method to show number of messages
    )
    list_filter = (
        'is_active',
        'created_at',
        'user', # Filter by the associated user
    )
    search_fields = (
        'id__icontains', # Search by part of the UUID (case-insensitive)
        'user__username__icontains', # Search by username (case-insensitive)
        'messages__message_text__icontains', # Search by message text
    )
    readonly_fields = (
        'id',
        'user',
        'created_at',
        'updated_at',
    )
    inlines = [ChatMessageInline]

    # Custom method to display username or "Anonymous"
    def user_display(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    user_display.short_description = "User" # Column header in admin

    # Custom method to display the number of messages in a session
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Message Count" # Column header in admin

    # To improve performance if you have many messages
    # You might want to select_related('user') in get_queryset for list_display
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optimise fetching user data for list_display
        return queryset.select_related('user')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'message_text_preview', 'timestamp')
    list_filter = ('sender', 'timestamp', 'session__is_active', 'session__user') # Filter by session, user
    search_fields = ('message_text__icontains', 'session__id__icontains', 'session__user__username__icontains')
    readonly_fields = ('session', 'sender', 'message_text', 'timestamp', 'products') # Messages should generally be read-only in admin

    def message_text_preview(self, obj):
        return obj.message_text[:75] + '...' if len(obj.message_text) > 75 else obj.message_text
    message_text_preview.short_description = "Message Preview"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('session', 'session__user') # Optimize fetching session and user data