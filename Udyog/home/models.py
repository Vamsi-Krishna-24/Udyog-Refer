
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model



class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        # lets Django authenticate with your USERNAME_FIELD (email)
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # identity
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    # your custom field
    ROLE_REFERRER = 'referrer'
    ROLE_REFEREE  = 'referee'
    ROLE_CHOICES  = [(ROLE_REFERRER, 'Referrer'), (ROLE_REFEREE, 'Referee')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True, default=None)

    # required by Django admin/auth
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    # is_superuser comes from PermissionsMixin (and becomes a DB column)

    USERNAME_FIELD  = "email"         # login by email
    REQUIRED_FIELDS = ["username"]    # asked when createsuperuser runs

    objects = UserManager()
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


class Referral_post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="referral_posts"
    )
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    referral_domains = models.CharField(max_length=100, blank=True, null=True, default="Not specified")
    job_description = models.TextField()
    experience_required = models.CharField(max_length=100)
    availability = models.CharField(max_length=100, blank=True, null=True)  # optional
    location = models.CharField(max_length=100)
    salary_expectation = models.CharField(max_length=100, blank=True, null=True)
    link_to_apply = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.role}"

# -----> EDIT your Jobs model like this
from django.db import models
class Job(models.Model):
    # auto 'id' stays as primary key
    source = models.CharField(max_length=50, db_index=True)                
    external_id = models.CharField(max_length=64, db_index=True)           
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, default="Remote")
    position = models.CharField(max_length=255)
    url = models.URLField()
    salary = models.CharField(max_length=255, blank=True, default="Not disclosed")
    description = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "external_id"], name="uniq_source_external")
        ]
    def __str__(self):
        return f"{self.company} – {self.position}"



#Defining a model to store the Seeker Request 

class SeekerRequest(models.Model):
    referral_post=models.ForeignKey(
        "Referral_post",
        on_delete=models.CASCADE,
        related_name="seeker_requests"
    )

    requester = models.ForeignKey(
        "home.User",
        on_delete=models.CASCADE,
        related_name="sent_requests"
    )

    referrer=models.ForeignKey(
        "home.User",
        on_delete=models.CASCADE,
        related_name="received_requests"
    )

    resume = models.FileField(upload_to= "media/", blank=True, null=True)

    STATUS_CHOICES=[
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )

    message = models.TextField(blank=True, null=True) 
    reason  = models.TextField(blank=True, null=True)

        # 🕒 Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("referral_post", "requester")

    def __str__(self):
        return f"{self.requester} → {self.referrer} ({self.status})"
    




#Model for Profile

User = get_user_model()

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True)  # auto from User on create
    title = models.CharField(max_length=100, blank=True)
    quote = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    linkedin = models.URLField()  # mandatory
    github = models.URLField(blank=True)
    other_link = models.URLField(blank=True)

    skills = models.JSONField(default=list, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        # Auto-fill name from user if empty
        if not self.name and hasattr(self.user, "name"):
            self.name = self.user.name
        elif not self.name:
            self.name = self.user.username
        super().save(*args, **kwargs)


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    role_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role_name} @ {self.company}"


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=100)
    link = models.URLField(blank=True)
    brief = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150)
    achievements = models.TextField(blank=True)

    def __str__(self):
        return f"{self.school} ({self.field_of_study})"



    
