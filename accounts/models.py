from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.conf import settings
from course.models import Course
from PIL import Image
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'email': 'email'}

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class PendingUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255) # store verification token

    def __str__(self):
        return self.email
        

class User(AbstractBaseUser, PermissionsMixin):
    STUDENT = "student"
    COURSE_CREATOR = "course_creator"
    MODERATOR = "moderator"

    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (COURSE_CREATOR, "Course Creator"),
        (MODERATOR, "Moderator"),
    ]
    AUTH_PROVIDERS = {
        'facebook': 'facebook',
        'google': 'google',
        'twitter': 'twitter', 
        'email': 'email'
    }

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    auth_provider = models.CharField(
        max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        ordering = ['created_at']


class EmailVerification(models.Model):
    short_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.short_id)