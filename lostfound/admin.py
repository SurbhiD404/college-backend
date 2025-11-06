from django.contrib import admin
from .models import Item, Chat

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'claimed']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id']
