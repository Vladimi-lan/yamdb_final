from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from .validators import name_me_validator, username_validator


class CustomUserManager(UserManager):
    def create_user(self, email, username, password=None,
                    first_name='', last_name='', bio='',
                    role='user'):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, role, bio):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            role=role,
            bio=bio,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        confirmation_code = default_token_generator.make_token(user)
        user.email_user(
            'Регистрация', f'confirmation_code: {confirmation_code}')
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN)
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator, name_me_validator],
        verbose_name='Имя пользователя',
        help_text='Имя пользователя'
    )
    email = models.EmailField('email address', max_length=254, unique=True)
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    bio = models.TextField(
        'bio',
        blank=True,
    )
    role = models.CharField(
        choices=ROLES, default=USER, max_length=50, verbose_name='role')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'role', 'bio']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    def set_status(self):
        """Set the user`s status."""
        if self.role == self.ADMIN:
            self.is_staff = True
        if self.role == self.MODERATOR:
            self.is_staff = True
        if self.role == self.USER:
            self.is_staff = False
        if self.is_superuser:
            self.is_active = True
            self.is_staff = True

    def save(self, *args, **kwargs):
        self.set_status()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username
