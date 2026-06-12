from django.contrib import admin
from .models import Note, VideoNote  # Yahan dono models shamil ho gaye

# 1. Ayesha ka code
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    search_fields = ('title', 'content')

# 2. Zunaira ka code (Aapka AI model register ho gaya)
admin.site.register(VideoNote)