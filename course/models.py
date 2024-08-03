from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Q
from django.dispatch import receiver
from .utils import unique_slug_generator
#from core.models import ActivityLog

LEVEL = (
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advanced", "Advanced"),
)
class ActivityLog(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.created_at}]{self.message}"
    
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Course(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, default='Untitled Course')
    code = models.CharField(max_length=200, unique=True, default='DEFAULT_CODE')
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    level = models.CharField(max_length=25, choices=LEVEL, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    is_elective = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"{self.title} ({self.code})"

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def is_current(self):
        return True 


class InstructorAssignment(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses_assigned")
    courses = models.ManyToManyField(Course, related_name="instructors")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.instructor.get_full_name()} - {self.courses.count()} courses"


class CourseMaterial(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    file = models.FileField(
        upload_to="course_materials/",
        help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
        validators=[FileExtensionValidator([
            "pdf", "docx", "doc", "xls", "xlsx", "ppt", "pptx", "zip", "rar", "7zip"
        ])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_extension_short(self):
        ext = self.file.name.split('.')[-1]
        mapping = {
            "doc": "word",
            "docx": "word",
            "pdf": "pdf",
            "xls": "excel",
            "xlsx": "excel",
            "ppt": "powerpoint",
            "pptx": "powerpoint",
            "zip": "archive",
            "rar": "archive",
            "7zip": "archive",
        }
        return mapping.get(ext, "unknown")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class CourseVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(
        upload_to="course_videos/",
        help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
        validators=[FileExtensionValidator([
            "mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"
        ])]
    )
    description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video_detail", kwargs={"slug": self.slug})

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user} enrolled in {self.course}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.course}"


# Signals
@receiver(post_save, sender=Course)
def log_course_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The course '{instance}' has been {verb}.")

@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The course '{instance}' has been deleted.")

@receiver(post_save, sender=CourseMaterial)
def log_material_save(sender, instance, created, **kwargs):
    verb = "uploaded" if created else "updated"
    ActivityLog.objects.create(message=f"The material '{instance.title}' has been {verb} for course '{instance.course}'.")

@receiver(post_delete, sender=CourseMaterial)
def log_material_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The material '{instance.title}' for course '{instance.course}' has been deleted.")

@receiver(post_save, sender=CourseVideo)
def log_video_save(sender, instance, created, **kwargs):
    verb = "uploaded" if created else "updated"
    ActivityLog.objects.create(message=f"The video '{instance.title}' has been {verb} for course '{instance.course}'.")

@receiver(post_delete, sender=CourseVideo)
def log_video_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The video '{instance.title}' for course '{instance.course}' has been deleted.")
