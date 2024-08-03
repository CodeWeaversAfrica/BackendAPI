from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView,
    CourseListView, CourseDetailView,
    CourseMaterialListView, CourseMaterialDetailView,
    CourseVideoListView, CourseVideoDetailView,
    EnrollmentListView, EnrollmentDetailView,
    ReviewListView, ReviewDetailView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course-materials/', CourseMaterialListView.as_view(), name='course-material-list'),
    path('course-materials/<int:pk>/', CourseMaterialDetailView.as_view(), name='course-material-detail'),
    path('course-videos/', CourseVideoListView.as_view(), name='course-video-list'),
    path('course-videos/<int:pk>/', CourseVideoDetailView.as_view(), name='course-video-detail'),
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
