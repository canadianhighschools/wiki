from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from edit.models import Commit

from django.urls import reverse, path
from django.utils.html import format_html


@admin.register(Commit)
class CommitAdmin(admin.ModelAdmin):
    list_display = ["id", "section", "content", "revision", "date_created", "edit_status"]
    fields = ["section", "content", "revision"]

    def edit_status(self, obj):
        approve_url = reverse('admin:approve_url', kwargs={'id': obj.id})
        deny_url = reverse('admin:deny_url', kwargs={'id': obj.id})
        return format_html('<a class="button" href="{}">Approve</a><br><br><a class="button" href="{}">Deny</a>', approve_url, deny_url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:id>', self.approved_commit, name='approve_url'),
            path('deny/<int:id>', self.denied_commit, name='deny_url'),
        ]
        return custom_urls + urls

    def approved_commit(self, request, id):
        print ('approved', id)

    def denied_commit(self, request, id):
        print ('denied', id)