from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_MIN_LENGTH = 5
    USERNAME_MAX_LENGTH = 30
    USERNAME_REGEX = r'^[a-zA-Z0-9]+[_\-]*[a-zA-Z0-9]'
    USERNAME_VALIDATOR = RegexValidator(USERNAME_REGEX)
    username = models.SlugField(
        _('username'),
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[USERNAME_VALIDATOR, MinLengthValidator(USERNAME_MIN_LENGTH)]
    )
    email = models.EmailField(_('email address'), max_length=200, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager() # Use default Django user manager as the field names
                            # are the same

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_username()

    def get_full_name(self):
        return self.__str__()

    def get_short_name(self):
        return self.__str__()
