from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at') # Dashboard par yeh columns dikhengi
    search_fields = ('title', 'content') # Search bar enable ho jayegafrom django.contrib import admin

# Register your models here.
