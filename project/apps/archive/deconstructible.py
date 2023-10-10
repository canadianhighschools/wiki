from django.utils.translation import gettext_lazy as _

import uuid
from django.utils.deconstruct import deconstructible


@deconstructible
class RenameFileToUUID:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename to UUID so it doesn't collide
        fp = f'{uuid.uuid4()}.{ext}'
        return fp


rename_file_to_uuid = RenameFileToUUID()