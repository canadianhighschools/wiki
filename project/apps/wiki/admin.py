from django.contrib import admin
from django.apps import apps

from django.contrib import admin
from .models import Category, Page, Revision

from apps.core.models import TextContent


def fetch_parent_as_path(parent):
    s = []
    while parent:
        s.insert(0, f'{parent.slug}')
        parent = parent.parent
        s[0] += '/'

    return ''.join(s)


class PageInline(admin.TabularInline):
    model = Page
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "path", "date_created", "date_modified"]
    inlines = [PageInline]

    def path(self, category: Category):
        return f'{fetch_parent_as_path(category.parent)}{category.slug}'

    fields = ["title", "slug", "description", "parent"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "path", "date_created", "date_modified"]

    def path(self, page: Page):
        return f'{fetch_parent_as_path(page.parent)}{page.slug}'

    fields = ["title", "slug", "description", "parent"]

admin.site.register(Revision)