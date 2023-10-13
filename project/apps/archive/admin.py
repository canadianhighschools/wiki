from django.contrib import admin
from .models import ArchiveDraft, ArchiveItem, ImageContent, PDFContent

admin.site.register(ArchiveDraft)
admin.site.register(ArchiveItem)
admin.site.register(ImageContent)
admin.site.register(PDFContent)