from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.conf import settings
import uuid

#from accounts.models import User

User = get_user_model()

JOB_TYPE_CHOICES = [
    ("1", "Full time"),
    ("2", "Part time"),
    ("3", "Internship"),
]

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class JobManager(models.Manager):
    def filled(self, *args, **kwargs):
        """Return jobs that are marked as filled."""
        return self.filter(filled=True, *args, **kwargs)

    def unfilled(self, *args, **kwargs):
        """Return jobs that are not filled."""
        return self.filter(filled=False, *args, **kwargs)

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE_CHOICES, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)  # Added ManyToManyField for tags
    vacancy = models.IntegerField(default=1)
    slug = models.SlugField(unique=True, editable=False)
    deadline = models.DateField(null=True)
    no_of_applicants = models.PositiveIntegerField(default=0)

    objects = JobManager()

    class Meta:
        ordering = ["-created_at"]  # Changed ordering to sort by newest first

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", args=[self.id])

    def __str__(self):
        return self.title

class Applicant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]  # Changed ordering to sort by newest first
        unique_together = ["user", "job"]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.job.title}"

    @property
    def get_status(self):
        status_dict = {1: "Pending", 2: "Accepted", 3: "Rejected"}
        return status_dict.get(self.status, "Unknown")

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(default=timezone.now)
    soft_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.job.title}"
