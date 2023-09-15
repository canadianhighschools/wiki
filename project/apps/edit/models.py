from django.db import models

from settings.base import AUTH_USER_MODEL

from apps.core.data.models import AbstractDatedModel


# A modification to a section of a revision
# status:
# 1000: denied 
# 1010: denied (must be edited / very conflicting)
# 1020: denied (abusive content, hatespeech, vandalism, automatically suspends contributor's commits)
# 2000: accepted 
# 2010: accepted (needs to be looked over by someone else, but for now it works)
# 2020: accepted (temporarily)
# 2030: accepted (but heavily modified)
# 3000: suspended (this commit is unable to be approved until unsuspended)
class Commit(models.Model, AbstractDatedModel):
    section = models.CharField(max_length=255, verbose_name="Edited Section")
    content = models.OneToOneField('data.TextContent', on_delete=models.PROTECT)
    revision = models.ForeignKey('data.Revision', on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(verbose_name="Status", default=0)
    approver = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Approver", null=True, blank=True, auto_created=True, editable=False, related_name="approver")
    contributor = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Contributor", auto_created=True, editable=False, related_name="contributor")
    edited = models.BooleanField(default=False, verbose_name="Edited", auto_created=True, editable=False)

    def __str__(self):
        return self.section

    class Meta:
        db_table = 'Commit'
        verbose_name = 'Commit'
        verbose_name_plural = 'Commits'