from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.translation import gettext_lazy as _

from .models import PDFContent

@receiver(pre_delete, sender=PDFContent)
def delete_pdf_file(sender, instance, *args, **kwargs):
    """ Deletes external files on `post_delete` """
    if instance.file:
        instance.file.delete()