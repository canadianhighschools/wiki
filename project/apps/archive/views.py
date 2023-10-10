from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView

from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ArchiveItem
from .forms import ArchiveItemForm

prefix = 'archive/'


class IndexView(generic.TemplateView):
    template_name = prefix + 'index.html'

    def get(self, request, *args, **kwargs): 
        return render(request, self.template_name, {'archive_items': ArchiveItem.objects.all()}) 

    

class ItemView(generic.DetailView):
    model = ArchiveItem
    template_name = prefix + 'detail.html'
    pk_url_kwarg = 'item_id'


class ArchiveItemFormView(LoginRequiredMixin, CreateView):
    template_name = prefix + 'upload.html'
    form_class = ArchiveItemForm
    success_url = 'success/'
