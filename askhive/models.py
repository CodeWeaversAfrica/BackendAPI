from django.db import models
from django.conf import settings
from autoslug import AutoSlugField

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    """
    Category model to classify questions.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    """
    Model for a question.
    """
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def total_votes(self):
        return self.answers.aggregate(total_votes=models.Sum('votes__value'))['total_votes'] or 0

    class Meta:
        ordering = ['-created_at']

class Answer(models.Model):
    """
    Model for an answer to a question.
    """
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, )

    def __str__(self):
        return f'Answer by {self.author} on {self.question.title}'

    def total_votes(self):
        return self.votes.aggregate(total_votes=models.Sum('value'))['total_votes'] or 0

    class Meta:
        ordering = ['-created_at']

class Vote(models.Model):
    """
    Model for a vote on an answer.
    """
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='votes', on_delete=models.CASCADE)
    value = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'answer')

class Comment(models.Model):
    """
    Model for a comment on an answer.
    """
    answer = models.ForeignKey(Answer, related_name='askhive_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='askhive_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.answer}'

