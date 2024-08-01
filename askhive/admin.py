from django.contrib import admin
from .models import Question, Answer, Vote, Comment

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('answer', 'author', 'content', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
