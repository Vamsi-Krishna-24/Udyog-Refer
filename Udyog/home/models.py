
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        # -----> ensure role is optional
        extra_fields.setdefault('role', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):  # -----> add PermissionsMixin for admin perms
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    ROLE_REFERRER = 'referrer'
    ROLE_REFEREE  = 'referee'
    # -----> ADD THIS FIELD
    ROLE_CHOICES = ((ROLE_REFERRER, 'Referrer'), (ROLE_REFEREE, 'Referee'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True, default=None)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email
    
class ReferralReq(models.Model):
    phone_number=models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    Linkdin_URL = models.URLField(max_length=200)
    Github_URL = models.URLField(max_length=200)
    Bio =   models.TextField()
    Currently_working = models.CharField(
        max_length=3,
        choices=[('yes', 'Yes'), ('no', 'No')]
    )
    


class Referrer(models.Model):    
    company_name = models.CharField(max_length=100)
    your_role = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    mail_id= models.EmailField(max_length=100)
    linkedin_url = models.URLField(max_length=200)
    github_url = models.URLField(max_length=200)
    bio =   models.TextField()
    
   


    
