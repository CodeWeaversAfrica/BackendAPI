from rest_framework.permissions import BasePermission
from .models import Question, Answer, Comment, Vote

class IsAdminOrModerator(BasePermission):
    """
    Custom permission to only allow admin or moderator users to access or modify certain views.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and check if they are admin or moderator
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser or request.user.role == 'moderator')

class IsQuestionAuthor(BasePermission):
    """
    Custom permission to only allow the author of a question to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Question):
            return obj.author == request.user
        return False

class IsAnswerAuthor(BasePermission):
    """
    Custom permission to only allow the author of an answer to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Answer):
            return obj.author == request.user
        return False

class IsCommentAuthor(BasePermission):
    """
    Custom permission to only allow the author of a comment to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Comment):
            return obj.author == request.user
        return False
"""
class IsVoteOwner(BasePermission):

    #Custom permission to only allow the user who created a vote to access or #modify it.
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Vote):
            return obj.user == request.user
        return False
"""

