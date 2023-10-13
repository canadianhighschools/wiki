from django.db import models

from apps.core.models import AbstractDatedModel, AbstractDescriptiveItem, ExternalContent, ContributionMixin, ApproverMixin

from .validators import validate_pdf_file_extension
from apps.core.deconstructible import rename_file_to_uuid


class ImageContent(ExternalContent):
    file = models.ImageField('file', upload_to=rename_file_to_uuid)
    
    class Meta:
        db_table = 'ImageContent'
        verbose_name = 'Image Content'
        verbose_name_plural = 'Image Contents'



class PDFContent(ExternalContent):
    file = models.FileField('file', upload_to=rename_file_to_uuid, validators=[validate_pdf_file_extension], storage='archive')
    
    class Meta:
        db_table = 'PDFContent'
        verbose_name = 'PDF Content'
        verbose_name_plural = 'PDF Contents'

    


class ArchiveDraft(AbstractDatedModel, AbstractDescriptiveItem, ContributionMixin):
    pdf = models.OneToOneField(PDFContent, on_delete=models.CASCADE, verbose_name="PDF", related_name='draft_pdf')

    class Meta:
        db_table = 'ArchiveDraft'
        verbose_name = 'Archive Draft'
        verbose_name_plural = 'Archive Drafts'

    def __str__(self):
        return f'{self.id}. {self.title}'
    

class ArchiveItem(AbstractDatedModel, AbstractDescriptiveItem, ApproverMixin):
    img = models.OneToOneField(ImageContent, on_delete=models.CASCADE, verbose_name="Snapshot", related_name='snapshot', null=True, auto_created=True)
    pdf = models.OneToOneField(PDFContent, on_delete=models.CASCADE, verbose_name="PDF", related_name='item_pdf')

    class Meta:
        db_table = 'ArchiveItem'
        verbose_name = 'Archive Item'
        verbose_name_plural = 'Archive Items'