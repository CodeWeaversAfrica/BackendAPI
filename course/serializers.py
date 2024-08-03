from rest_framework import serializers
from .models import Category, Course, CourseMaterial, CourseVideo, Enrollment, Review
from accounts.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    lecturers = UserSerializer(many=True, read_only=True) 

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'description', 'category', 'lecturers', 'credits', 'semester', 'year']

class CourseMaterialSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseMaterial
        fields = ['id', 'title', 'file', 'course', 'uploaded_at']

class CourseVideoSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseVideo
        fields = ['id', 'title', 'video_file', 'course', 'uploaded_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'course', 'review', 'rating', 'created_at', 'updated_at']
