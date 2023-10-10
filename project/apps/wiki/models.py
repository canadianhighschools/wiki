from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractDatedModel



def validate_slug(value):    
    for l in value:
        if (l.isupper()):
            raise ValidationError(
                "Use only lower-case letters please!",
                params={'value': value},
            )
        elif (l in ['_', ' ']):
            raise ValidationError(
                "Spaces and underscores are forbidden, use hypens (-) instead.",
                params={'value': value},
            )






# A wrapper for a category - supports nesting.
class Category(AbstractDatedModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    slug = models.CharField(max_length=255, null=True, verbose_name="Slug", validators=[validate_slug])
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Parent", related_name='child_categories')

    class Meta:
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.id}. {self.title}'


# A wrapper for a page
class Page(AbstractDatedModel):
    title = models.CharField("title", max_length=255)
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    slug = models.CharField(max_length=255, verbose_name="Slug", validators=[validate_slug])
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Category", related_name="child_pages")

    class Meta:
        db_table = 'Page'
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return f'{self.id}. {self.title}'



# A page revision / points to the sections
class Revision(AbstractDatedModel):
    order = models.IntegerField(verbose_name="Order #", default=0)
    # could potentially be a rollback and not a content revision

    # another many to one key because multiple revisions could rollback to one revision
    # but one revision will never rollback to many
    rollback = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='rollbacks')
    
    # one content per revision, unique
    content = models.OneToOneField('TextContent', on_delete=models.PROTECT, verbose_name="Text Content", null=True, blank=True)
    page = models.ForeignKey('Page', on_delete=models.PROTECT, verbose_name="Page", related_name="revisions")

    def __str__(self):
        return f'{self.page.title} Revision #{self.order}'

    class Meta:
        db_table = 'Revision'
        verbose_name = 'Revision'
        verbose_name_plural = 'Revisions'

        # either rollback or content must not be null
        # taken from https://stackoverflow.com/questions/53085645/django-one-of-2-fields-must-not-be-null
        constraints = [
            models.CheckConstraint(
                check=Q(rollback__isnull=False) | Q(content__isnull=False),
                name='not_both_null'
            )
            # TODO add constraint to make order unique among models?
        ]
        



