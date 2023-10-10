from django.db import models

from django.contrib.auth.models import Group, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from django.contrib.auth.validators import UnicodeUsernameValidator


class PermissionGroup(Group):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'



class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    
    nickname = models.CharField(_("nickname"), max_length=255)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    # email not required unless you register as a volunteer, then it is.
    # literally less than pennies even at our highest estimations of users like, ever
    REQUIRED_FIELDS = ["nickname"]

    volunteer = models.OneToOneField('core.Volunteer', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)



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

    volunteer = models.OneToOneField('core.Volunteer', on_delete=models.PROTECT, null=True, blank=True)