from django.contrib import admin
from .models import *


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'farmer')
    list_display_links = ('id',)
    search_fields = ('id', 'name',)

admin.site.register(Item, ItemAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password', 'address', 'phone_number', 'card')
    list_display_links = ('id',)
    search_fields = ('id', 'name')

admin.site.register(User, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'text', 'created_at')
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Message, MessageAdmin)

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Chat, ChatAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'rate', 'text')
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Comment, CommentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Order, OrderAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(OrderItems, OrderItemsAdmin)