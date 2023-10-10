from django.db import models

from apps.core.models import AbstractDatedModel, ExternalContent, StandardUserPermissionMixin

from taggit.managers import TaggableManager

from .validators import validate_pdf_file_extension
from .deconstructible import rename_file_to_uuid


class ImageContent(ExternalContent):
    file = models.ImageField('file', upload_to=rename_file_to_uuid)
    
    class Meta:
        db_table = 'ImageContent'
        verbose_name = 'Image Content'
        verbose_name_plural = 'Image Contents'



class PDFContent(ExternalContent):
    file = models.FileField('file', upload_to=rename_file_to_uuid, validators=[validate_pdf_file_extension])
    
    class Meta:
        db_table = 'PDFContent'
        verbose_name = 'PDF Content'
        verbose_name_plural = 'PDF Contents'

class ArchiveItem(AbstractDatedModel, StandardUserPermissionMixin):
    title = models.CharField(max_length=255, verbose_name="Title")
    img = models.OneToOneField(ImageContent, on_delete=models.CASCADE, verbose_name="Snapshot", related_name='snapshot', null=True, auto_created=True)
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    pdf = models.OneToOneField(PDFContent, on_delete=models.CASCADE, verbose_name="PDF", related_name='PDF')
    tags = TaggableManager()

    class Meta:
        db_table = 'ArchiveItem'
        verbose_name = 'Archive Item'
        verbose_name_plural = 'Archive Items'

    def __str__(self):
        return f'{self.id}. {self.title}'