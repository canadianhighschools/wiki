from django import forms

from .models import ArchiveItem
from apps.core.models import PDFContent

from .validators import validate_pdf_file_extension


class ArchiveItemForm(forms.ModelForm):
    class Meta:
        model = ArchiveItem
        fields = ['title', 'description', 'tags']

    submitted_pdf_file = forms.FileField(label='Upload a PDF', allow_empty_file=False, validators=[validate_pdf_file_extension])

    def save(self, commit=True):
        # create our new PDFContent
        submitted_pdf_file = self.cleaned_data.get('submitted_pdf_file')
        pdf = PDFContent(file=submitted_pdf_file)
        pdf.save()
        
        # set this ArchiveItem's value to it
        self.instance.pdf = pdf

        # save
        return super().save(commit=commit)