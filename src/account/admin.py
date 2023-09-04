from django.contrib import admin

from .models import PermissionGroup, User

admin.site.register(PermissionGroup)
admin.site.register(User)