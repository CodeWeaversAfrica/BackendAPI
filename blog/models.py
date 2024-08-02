from django.db import models
from django.conf import settings
from autoslug import AutoSlugField

class Category(models.Model):
    """
    Category model to classify blog posts.
    """
    TECH_CHOICES = [
        ('Technology', 'Technology'),
        ('Programming', 'Programming'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Data Science', 'Data Science'),
        ('AI & ML', 'AI & ML'),
        ('Gadgets', 'Gadgets'),
        ('Software Development', 'Software Development'),
        ('Hardware', 'Hardware'),
        ('Networking', 'Networking'),
        ('Cloud Computing', 'Cloud Computing'),
        ('DevOps', 'DevOps'),
    ]

    name = models.CharField(max_length=100, choices=TECH_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    """
    Blog Post model with title, content, author, category, and like functionality.
    """
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to custom User
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def summary(self):
        return self.content[:100]

    def reading_time(self):
        total_words = len(self.content.split())
        reading_time = round(total_words / 200)
        if reading_time == 0:
            return '<1 min read'
        return f'{reading_time} min read'

    def comment_count(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    """
    Comment model for blog posts.
    """
    blog = models.ForeignKey(Blog, related_name='blog_comments', on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_comments')  # Reference to custom User
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'

    def date_format(self):
        return self.created_at.strftime("%d-%b-%y, %I:%M %p")

