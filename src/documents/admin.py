from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at", "updated_at")  # ✅ add here
    list_filter = ("active", "created_at", "updated_at")  # optional: filter by updated time
    search_fields = ("title", "content")  # optional: make searchable