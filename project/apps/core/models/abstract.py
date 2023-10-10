from django.db import models
from config.settings.base import AUTH_USER_MODEL

class AbstractDatedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False, verbose_name="Creation Date")
    date_modified = models.DateTimeField(auto_now=True, auto_created=True, editable=False, verbose_name="Last Modified")

    class Meta:
        abstract = True


class StandardUserPermissionMixin:
    approver = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Approver", null=True, blank=True, auto_created=True, editable=False, related_name="approver")
    contributor = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Contributor", auto_created=True, editable=False, related_name="contributor")
    edited = models.BooleanField(default=False, verbose_name="Edited", auto_created=True, editable=False)
