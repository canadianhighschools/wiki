from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ArchiveItem, ArchiveDraft
from .forms import ArchiveDraftForm

prefix = 'archive/'


class IndexView(generic.TemplateView):
    template_name = prefix + 'base.html'

    def get(self, request, *args, **kwargs): 
        return render(request, self.template_name, {'archive_drafts': ArchiveDraft.objects.all(), 'archive_items': ArchiveItem.objects.all()}) 
    

class DraftView(generic.DetailView):
    model = ArchiveDraft
    template_name = prefix + 'detail.html'
    pk_url_kwarg = 'pk'

class ItemView(generic.DetailView):
    model = ArchiveItem
    template_name = prefix + 'detail.html'
    pk_url_kwarg = 'pk'


class ArchiveDraftFormView(LoginRequiredMixin, CreateView):
    template_name = prefix + 'upload.html'
    form_class = ArchiveDraftForm
    success_url = 'success/'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ArchiveDraftForm, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class SuccessView(generic.TemplateView):
    template_name = prefix + 'success.html'

    def get(self, request, *args, **kwargs): 
        return render(request, self.template_name, {'archive_item': ArchiveItem.objects.all()}) 
