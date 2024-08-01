from rest_framework import serializers
from .models import Question, Answer, Vote, Comment

class QuestionSerializer(serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()
    answer_count = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Question
        fields = ['id', 'title', 'slug', 'content', 'created_at', 'updated_at', 'author', 'total_votes', 'answer_count', 'category_name']

    def get_total_votes(self, obj):
        return obj.total_votes()

    def get_answer_count(self, obj):
        return obj.answers.count()

class AnswerSerializer(serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'content', 'created_at', 'updated_at', 'author', 'total_votes', 'author_name']

    def get_total_votes(self, obj):
        return obj.total_votes()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'answer', 'value']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='author.username')
    user_photo = serializers.ReadOnlyField(source='author.photo.url')

    class Meta:
        model = Comment
        fields = ['id', 'username', 'content', 'created_at', 'user_photo']
