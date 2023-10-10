from django.contrib import admin
from django.contrib.auth.models import Group
from .models import PermissionGroup, User, Volunteer, TextContent, ImageContent, PDFContent, Institution

admin.site.unregister(Group)
admin.site.register(PermissionGroup)
admin.site.register(User)
admin.site.register(Volunteer)
admin.site.register(Institution)
admin.site.register(TextContent)
admin.site.register(ImageContent)
admin.site.register(PDFContent)