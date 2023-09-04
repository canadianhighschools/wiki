from django.db import models


from django.contrib.auth.models import Group, AbstractUser
from django.utils.translation import gettext_lazy as _

class PermissionGroup(Group):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class User(AbstractUser):
    groups = models.ManyToManyField(
        PermissionGroup,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their levels."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



# class User(AbstractBaseUser, PermissionsMixin):
#     username_validator = UsernameValidator()

#     username = models.CharField(
#         _("username"),
#         max_length=40,
#         unique=True,
#         help_text=_(
#             "Required. 40 characters or fewer. Lower-case letters, digits and -/+/. only."
#         ),
#         validators=[username_validator],
#         error_messages={
#             "unique": _("A user with that username already exists."),
#         },
#     )

#     display_name = models.CharField(_("display name"), max_length=50)

#     email = models.EmailField(_("email address"), blank=True, default="")

#     is_staff = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )

#     is_active = models.BooleanField(
#         _("active"),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

#     objects = UserManager()

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["username", "display_name"]

#     class Meta:
#         verbose_name = "User"
#         verbose_name = "User"
#         verbose_name_plural = "Users"

#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)

#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between.
#         """
#         full_name = "%s %s" % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.first_name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         pass
#         # send_mail(subject, message, from_email, [self.email], **kwargs)



class Volunteer(models.Model):
    first_name = models.CharField("core.first_name", max_length=150)
    last_name = models.CharField("last name", max_length=150)
    hours = models.SmallIntegerField(default=0)
    platform = models.CharField("platform", max_length=255)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        db_table = 'Volunteer'
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteers'


