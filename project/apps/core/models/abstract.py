from django.db import models
from config.settings.base import AUTH_USER_MODEL

from taggit.managers import TaggableManager

class AbstractDatedModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False, verbose_name="Creation Date")
    date_modified = models.DateTimeField(auto_now=True, auto_created=True, editable=False, verbose_name="Last Modified")

    class Meta:
        abstract = True


class AbstractDescriptiveItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    tags = TaggableManager()

    class Meta:
        abstract = True


class ContributionMixin:
    contributor = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Contributor", auto_created=True, editable=False, related_name="contributor")

class ApproverMixin:
    approver = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Approver", null=True, auto_created=True, editable=False, related_name="approver")
    edited = models.BooleanField(default=False, verbose_name="Edited", auto_created=True, editable=False)
