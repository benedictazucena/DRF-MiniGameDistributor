from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy  as _
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, birthday, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, birthday, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(email=self.normalize_email(email), birthday=birthday, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, birthday, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, birthday, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, birthday, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    birthday = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birthday']

    def clean(self):
        super().clean()
        if self.birthday and self.get_age() < 18:
            raise ValidationError(_('User must be 18 years or older.'))

    def get_age(self):
        if self.birthday:
            today = datetime.date.today()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return None
