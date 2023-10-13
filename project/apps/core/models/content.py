from django.db import models
from django.utils.translation import gettext_lazy as _

from ..deconstructible import rename_file_to_uuid



# All text content of any kind: compressed, local, on another server.
# Flags
# 000: Text is on this database and fully readable
# 001: Must be decompressed using gzip
# 010: Stored on another database (value is an ip)
# 100: Always cache
class TextContent(models.Model):
    text = models.TextField()
    flags = models.SmallIntegerField(default=0, auto_created=True)

    def __str__(self):
        v = self.text
        return f'{self.id}. {v[:50]}...' if len(v) > 50 else v

    class Meta:
        db_table = 'TextContent'
        verbose_name = 'Text Content'
        verbose_name_plural = 'Text Contents'



# @receiver(models.signals.post_delete, sender=ProductImage)
# def delete_file(sender, instance, *args, **kwargs):
#     """ Deletes image files on `post_delete` """
#     if instance.image:
#         _delete_file(instance.image.path)


# external content
class ExternalContent(models.Model):
    file = models.FileField('file', upload_to=rename_file_to_uuid)
    flags = models.SmallIntegerField(default=0, auto_created=True)

    def __str__(self):
        return f'{self.id}. {self.file.name}'
    
    class Meta:
        abstract = True