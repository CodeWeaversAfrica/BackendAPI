from rest_framework.permissions import BasePermission

class IsAuthenticatedAndVerified(BasePermission):
    """
    Custom permission to check if the user is authenticated, active, and verified.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            user and 
            user.is_authenticated and 
            user.is_active and 
            user.is_verified
        )

class IsRole(BasePermission):
    #Custom permission to check if the user has a specific role.
    def __init__(self, role):
        self.role = role

    def has_permission(self, request, view):
        user = request.user
        return (
            user and 
            user.is_authenticated and 
            user.is_active and 
            user.is_verified and
            user.role == self.role
        )

class IsStudent(IsRole):
    def __init__(self):
        super().__init__(role="student")

class IsCourseCreator(IsRole):
    def __init__(self):
        super().__init__(role="course_creator")

class IsModerator(IsRole):
    def __init__(self):
        super().__init__(role="moderator")

class IsAdmin(BasePermission):
    #Custom permission to check if the user is an admin.
    def has_permission(self, request, view):
        user = request.user
        return (
            user and 
            user.is_authenticated and 
            user.is_active and 
            user.is_verified and 
            user.is_admin
        )