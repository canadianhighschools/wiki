import os
from django.core.exceptions import ValidationError

def validate_file_extension(value, extensions, msg='Unsupported file extension!'):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in extensions:
        raise ValidationError(msg)

def validate_pdf_file_extension(value):
    return validate_file_extension(value, ['.pdf'], msg='File must be .pdf')