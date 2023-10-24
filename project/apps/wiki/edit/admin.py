from django.contrib import admin
# from django.apps import apps
# from django.utils.functional import LazyObject
# from django.utils.module_loading import import_string


# from django import forms
# from django.contrib import admin

# from .models import Commit

# from django.urls import reverse, path
# from django.utils.html import format_html



# class EditSite(LazyObject):
#     def _setup(self):
#         AdminSiteClass = import_string(apps.get_app_config("admin").default_site)
#         self._wrapped = AdminSiteClass()

#     def __repr__(self):
#         return repr(self._wrapped)
    

# site = EditSite()


# @admin.register(Commit)
# class CommitAdmin(admin.ModelAdmin):
#     list_display = ["id", "section", "content", "revision", "date_created", "edit_status"]
#     fields = ["section", "content", "revision"]

#     def edit_status(self, obj):
#         approve_url = reverse('admin:approve_url', kwargs={'id': obj.id})
#         deny_url = reverse('admin:deny_url', kwargs={'id': obj.id})
#         return format_html('<a class="button" href="{}">Approve</a><br><br><a class="button" href="{}">Deny</a>', approve_url, deny_url)

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('approve/<int:id>', self.approved_commit, name='approve_url'),
#             path('deny/<int:id>', self.denied_commit, name='deny_url'),
#         ]
#         return custom_urls + urls

#     def approved_commit(self, request, id):
#         print ('approved', id)

#     def denied_commit(self, request, id):
#         print ('denied', id)
