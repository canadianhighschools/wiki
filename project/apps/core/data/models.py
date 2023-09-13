from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



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



class AbstractDatedModel:
    date_created = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False, verbose_name="Creation Date")
    date_modified = models.DateTimeField(auto_now=True, auto_created=True, editable=False, verbose_name="Last Modified")



# A wrapper for a category - supports nesting.
class Category(models.Model, AbstractDatedModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    slug = models.CharField(max_length=255, null=True, verbose_name="Slug", validators=[validate_slug])
    parent = models.OneToOneField('self', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Parent")

    class Meta:
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.id}. {self.title}'


# A wrapper for a page
class Page(models.Model, AbstractDatedModel):
    title = models.CharField("title", max_length=255)
    description = models.CharField(max_length=32767, default="", blank=True, verbose_name="Description")
    slug = models.CharField(max_length=255, verbose_name="Slug", validators=[validate_slug])
    order = models.IntegerField(default=-1, auto_created=True, editable=False, verbose_name="Current Revision")
    parent = models.OneToOneField('Category', on_delete=models.PROTECT, verbose_name="Category")

    class Meta:
        db_table = 'Page'
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return f'{self.id}. {self.title}'



# A page revision / points to the sections
class Revision(models.Model, AbstractDatedModel):
    order = models.IntegerField(verbose_name="Order #", default=0, auto_created=True, editable=False)
    rollback = models.BooleanField(verbose_name="Is Rollback?", default=False, auto_created=True, editable=False)
    content = models.OneToOneField('TextContent', on_delete=models.PROTECT, verbose_name="Text Content")
    page = models.ForeignKey('Page', on_delete=models.PROTECT, verbose_name="Page", related_name="revisions")

    def __str__(self):
        return f'{self.page.title} Revision #{self.order}'

    class Meta:
        db_table = 'Revision'
        verbose_name = 'Revision'
        verbose_name_plural = 'Revisions'



# All text content of any kind: compressed, local, on another server.
# Flags
# 000: Text is on this database and fully readable
# 001: Must be decompressed using gzip
# 010: Stored on another database (value is an ip)
# 100: Always cache
class TextContent(models.Model):
    text = models.TextField()
    flags = models.SmallIntegerField(default=0)

    def __str__(self):
        v = self.text
        return f'{v[:50]}...' if len(v) > 50 else v

    class Meta:
        db_table = 'TextContent'
        verbose_name = 'Text'
        verbose_name_plural = 'Text'