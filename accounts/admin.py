from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password', 'address', 'phone_number', 'card')
    list_display_links = ('id',)
    search_fields = ('id', 'name')

admin.site.register(User, UserAdmin)