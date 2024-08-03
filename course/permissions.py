from rest_framework.permissions import BasePermission

class IsLecturer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_lecturer

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_student
