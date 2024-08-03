from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Job, Applicant, Tag

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    job_tags = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_job_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data if obj.tags.exists() else []

class DashboardJobSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    job_tags = serializers.SerializerMethodField()
    total_candidates = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_job_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data if obj.tags.exists() else []

    def get_total_candidates(self, obj):
        return obj.applicants.count()

class NewJobSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = "__all__"

class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ("job", "comment")

class ApplicantSerializer(serializers.ModelSerializer):
    applied_user_id = serializers.IntegerField(source='user.id', read_only=True)
    applied_user_username = serializers.CharField(source='user.username', read_only=True)
    applied_user_email = serializers.EmailField(source='user.email', read_only=True)
    applied_user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    applied_user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    job = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = ("id", "job", "applied_user_id", "applied_user_username", "applied_user_email", "applied_user_first_name", "applied_user_last_name", "status", "created_at", "comment")

    def get_status(self, obj):
        return obj.get_status

    def get_job(self, obj):
        return JobSerializer(obj.job).data

class AppliedJobSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    applicant = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_applicant(self, obj):
        user = self.context.get("request").user
        try:
            applicant = Applicant.objects.get(user=user, job=obj)
            return ApplicantSerializer(applicant).data
        except Applicant.DoesNotExist:
            return None
