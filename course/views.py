from rest_framework import viewsets, generics, status
from accounts.permissions import IsAuthenticatedAndVerified
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Category, Course, CourseMaterial, CourseVideo, Enrollment, Review
from .serializers import (
    CategorySerializer,
    CourseSerializer,
    CourseMaterialSerializer,
    CourseVideoSerializer,
    EnrollmentSerializer,
    ReviewSerializer
)
from .permissions import IsLecturer, IsStudent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedAndVerified]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['id', 'title']

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedAndVerified]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'code']
    ordering_fields = ['id', 'title', 'code']

    @action(detail=True, methods=['post'], permission_classes=[IsLecturer])
    def assign_lecturer(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        lecturer_id = request.data.get('lecturer_id')
        if not lecturer_id:
            return Response({'detail': 'lecturer_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Add logic to assign lecturer to course
        course.lecturers.add(lecturer_id)
        return Response({'detail': 'Lecturer assigned successfully.'}, status=status.HTTP_200_OK)

class CourseMaterialViewSet(viewsets.ModelViewSet):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    @action(detail=True, methods=['post'], permission_classes=[IsLecturer])
    def upload_material(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseVideoViewSet(viewsets.ModelViewSet):
    queryset = CourseVideo.objects.all()
    serializer_class = CourseVideoSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    @action(detail=True, methods=['post'], permission_classes=[IsLecturer])
    def upload_video(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Enrollment.objects.filter(user=user)
        elif user.is_lecturer:
            return Enrollment.objects.filter(course__in=user.courses_assigned.all())
        return Enrollment.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsStudent])
    def enroll(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        student = request.user.student
        if Enrollment.objects.filter(course=course, user=student).exists():
            return Response({'detail': 'Already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
        Enrollment.objects.create(course=course, user=student)
        return Response({'detail': 'Enrolled successfully.'}, status=status.HTTP_201_CREATED)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Review.objects.filter(user=user)
        elif user.is_lecturer:
            return Review.objects.filter(course__in=user.courses_assigned.all())
        return Review.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsStudent])
    def submit_review(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        student = request.user.student
        review_text = request.data.get('review')
        if not review_text:
            return Response({'detail': 'Review text is required.'}, status=status.HTTP_400_BAD_REQUEST)
        Review.objects.create(course=course, user=student, review=review_text)
        return Response({'detail': 'Review submitted successfully.'}, status=status.HTTP_201_CREATED)
