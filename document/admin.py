from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')  # Display columns in admin panel
    search_fields = ('file',)  # Search by file name
    list_filter = ('uploaded_at',)  # Filter by upload date
from .models import Prompt

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("text", "response", "created_at")  # Fields to display in admin panel
    search_fields = ("text", "response")  # Search bar for prompt & response
    list_filter = ("created_at",)  # Filter by date
