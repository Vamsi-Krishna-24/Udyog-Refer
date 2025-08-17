
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(AbstractBaseUser, PermissionsMixin):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

        # -----> add constants once
    ROLE_REFERRER = 'referrer'
    ROLE_REFEREE  = 'referee'
    ROLE_CHOICES = [(ROLE_REFERRER, 'Referrer'), (ROLE_REFEREE, 'Referee')]

    # -----> add the column
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True, default=None)


    def __str__(self):
        return self.email
    
class referal_req(models.Model):
    phone_number=models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    Linkdin_URL = models.URLField(max_length=200)
    Github_URL = models.URLField(max_length=200)
    Bio =   models.TextField()


class Referer(models.Model):    
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


    
