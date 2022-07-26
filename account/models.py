"""
 This default model provided by django might not be sufficient as we will have to store numeriouss data about the customer. 
 So we can either go ahead and extend thi user model or we can use a completly different user model.
 Here we will go ahead and build upon/extend the BaseUserManager to overwrite the account management of say superuser
 The AbstractBaseUSer help us to build our own user model. PermissionsMixin will build some default permissions to our tables
 Before making new migrations/creating DB, we have to delete old DB and migration files. Else we get an error
"""

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _   # This is used for translation
from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):   # this will specify how user data is saved in the DB

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)  # email is written first because it is the username now(we have set below check end of this page)

    def create_user(self, email, user_name, password, **other_fields):    # Email, username and password are the minimum parameters required to create user
        if not email:
            raise ValueError(_('You must provide an email address'))    # _ is used coz this might have to be translated into different language.

        email = self.normalize_email(email)   # This will check if the email is in proper format
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    # Delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.user_name
