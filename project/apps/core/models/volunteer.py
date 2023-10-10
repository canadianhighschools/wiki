from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils import timezone

class VolunteerPlatformTypes(models.TextChoices):
    MIDDLE_SCHOOL = 'MS', _('Middle School')
    HIGH_SCHOOL = 'HS', _('High School')
    COLLEGE = 'CO', _('College')
    UNIVERSITY = 'UN', _('University')


class Institution(models.Model):
    id = models.CharField("identifier", max_length=255, primary_key=True)
    name = models.CharField("name", max_length=255)
    platform = models.CharField(
        max_length=2,
        choices=VolunteerPlatformTypes.choices,
        default=VolunteerPlatformTypes.HIGH_SCHOOL,
    )

    def get_platform_type(self) -> VolunteerPlatformTypes:
        return VolunteerPlatformTypes[self.level]
    
    def __str__(self) -> str:
        return f'{self.id} | {self.name}'


class Volunteer(models.Model):
    first_name = models.CharField("first_name", max_length=150)
    last_name = models.CharField("last_name", max_length=150)
    hours = models.SmallIntegerField(default=0)
    last_hours_gained = models.DateTimeField(auto_created=True, default=timezone.now)
    institution = models.ForeignKey(Institution, related_name="volunteers", on_delete=models.PROTECT)
    # user-linked email ID is *required*

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        db_table = 'Volunteer'
