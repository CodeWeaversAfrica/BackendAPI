from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model including nested fields and computed properties.
    """
    total_likes = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    author_name = serializers.ReadOnlyField(source='author.username')
    author_photo = serializers.ReadOnlyField(source='author.photo.url')
    author_bio = serializers.ReadOnlyField(source='author.bio')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'created_at',
            'updated_at',
            'content',
            'image',
            'category',
            'likes',
            'total_likes',
            'summary',
            'author_name',
            'author_photo',
            'author_bio',
            'reading_time',
            'comment_count',
            'user_liked'
        ]

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_summary(self, obj):
        return obj.summary()

    def get_reading_time(self, obj):
        return obj.reading_time()

    def get_comment_count(self, obj):
        return obj.comment_count()

    def get_user_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user.is_active:
            return user in obj.likes.all()
        return False

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """
    username = serializers.ReadOnlyField(source='author.username')
    user_photo = serializers.ReadOnlyField(source='author.photo.url')

    class Meta:
        model = Comment
        fields = [
            'id',
            'username',
            'content',
            'created_at',
            'user_photo'
        ]

class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments.
    """
    class Meta:
        model = Comment
        fields = [
            'content',
            'post'
        ]
