from django.db import models

from apps.core import AbstractDatedModel, ExternalContent, StandardUserPermissionMixin

from taggit.managers import TaggableManager

class ArchiveItem(AbstractDatedModel, StandardUserPermissionMixin):
    title = models.CharField(max_length=255, verbose_name="Title")
    snapshot = models.OneToOneField(ExternalContent, on_delete=models.PROTECT, verbose_name="Snapshot")
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    content = models.OneToOneField(ExternalContent, on_delete=models.PROTECT, verbose_name="External Content")
    tags = TaggableManager()

    class Meta:
        db_table = 'ArchiveItem'
        verbose_name = 'Archive Item'
        verbose_name_plural = 'Archive Items'

    def __str__(self):
        return f'{self.id}. {self.title}'