from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.conf import settings
from course.models import Course
from PIL import Image
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'email': 'email'}


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    is_student = models.BooleanField(default=False)
    is_course_creator = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="profile_pictures/%Y/%m/%d/", default="default.png", null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_picture(self):
        try:
            return self.profile_picture.url
        except:
            no_picture = settings.MEDIA_URL + "default.png"
            return no_picture

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.profile_picture.url != settings.MEDIA_URL + "default.png":
            self.profile_picture.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['created_at']


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            qs = qs.filter(program__icontains=query).distinct()
        return qs


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    #courses = models.ManyToManyField('Course', related_name='students', blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    #program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    objects = StudentManager()

    def __str__(self):
        return self.student.get_full_name()

    @classmethod
    def get_gender_count(cls):
        males_count = cls.objects.filter(student__gender="male").count()
        females_count = cls.objects.filter(student__gender="female").count()
        return {"male": males_count, "female": females_count}

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)