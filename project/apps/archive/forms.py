from django import forms
from .models import ArchiveDraft, PDFContent

from .validators import validate_pdf_file_extension
from config.settings.archive import ALLOWED_TAGS


class ArchiveDraftForm(forms.ModelForm):
    class Meta:
        model = ArchiveDraft
        fields = ['title', 'description', 'tags']

    submitted_pdf_file = forms.FileField(label='Upload a PDF', allow_empty_file=False, validators=[validate_pdf_file_extension])

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop('user')
        super(ArchiveDraftForm, self).__init__(args, kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        tags = cleaned_data.get('tags')

        print ('taggos', tags)

        self.add_error('tag_not_found', 'Tags contain non-whitelisted tag!')

        return cleaned_data

    def save(self, commit=True):
        # create our new PDFContent
        submitted_pdf_file = self.cleaned_data.get('submitted_pdf_file')
        pdf = PDFContent(file=submitted_pdf_file)
        pdf.save()
        
        # set this ArchiveItem's value to it
        self.instance.pdf = pdf

        # assign contributor id
        self.instance.contributor = self.user

        # save
        return super().save(commit=commit)