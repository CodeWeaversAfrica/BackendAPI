from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Blog, Comment

class IsAdminOrModerator(BasePermission):
    """
    Custom permission to only allow admin or moderator users to access or modify certain views.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and check if they are admin or moderator
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser or request.user.role == 'moderator')

class IsAuthor(BasePermission):
    """
    Custom permission to only allow the author of a post to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Blog):
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
class IsObjectOwner(BasePermission):
    #Custom permission to only allow the owner of an object (Post or Comment) to access or modify it.

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Post) or isinstance(obj, Comment):
            return obj.author == request.user
        return False
"""        