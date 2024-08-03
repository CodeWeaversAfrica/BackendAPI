from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsAuthenticatedAndVerified
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from jobs.models import Job, Favorite, Applicant, Tag
from jobs.permissions import IsEmployee, IsEmployer
from jobs.metrics import requests_total
from jobs.serializers import (
    JobSerializer, 
    NewJobSerializer, 
    ApplicantSerializer, 
    ApplyJobSerializer, 
    TagSerializer
)

class EmployeeMyJobsListView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='employee_my_jobs', method='GET', user=request.user.username).inc()

        jobs = Job.objects.filter(applicants__user=request.user).distinct()
        serializer = JobSerializer(jobs, many=True)
        return Response({"jobs": serializer.data})

class EditProfileView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def put(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='edit_profile', method='PUT', user=request.user.username).inc()

        user = request.user
        data = request.data
        
        # Handle profile update logic manually
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        # Add more fields if necessary

        user.save()
        return Response({"status": "Profile updated successfully"})

class FavoriteListView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='favorite_list', method='GET', user=request.user.username).inc()

        favorites = Favorite.objects.filter(user=request.user, soft_deleted=False).select_related("job")
        favorites_data = [JobSerializer(favorite.job).data for favorite in favorites]
        return Response({"favorites": favorites_data, "total_favorites": favorites.count()})

class DashboardView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='dashboard', method='GET', user=request.user.username).inc()

        jobs = Job.objects.filter(user=request.user)
        serializer = JobSerializer(jobs, many=True)
        return Response({"jobs": serializer.data})

class ApplicantPerJobView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='applicant_per_job', method='GET', user=request.user.username).inc()

        job_id = kwargs.get("job_id")
        try:
            job = Job.objects.get(id=job_id)
            applicants = Applicant.objects.filter(job=job).order_by("id")
            applicants_data = ApplicantSerializer(applicants, many=True).data
            return Response({"job": JobSerializer(job).data, "applicants": applicants_data})
        except Job.DoesNotExist:
            return Response({"error": "Job does not exist"}, status=status.HTTP_404_NOT_FOUND)

class JobCreateView(APIView):
    permission_classes = [IsAuthenticatedAndVerified, IsEmployer]

    def post(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='job_create', method='POST', user=request.user.username).inc()

        serializer = NewJobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(user=request.user)
            tags = request.data.get("tags", [])
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                job.tags.add(tag)
            return Response({"status": "Job created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobUpdateView(APIView):
    permission_classes = [IsAuthenticatedAndVerified, IsEmployer]

    def put(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='job_update', method='PUT', user=request.user.username).inc()

        job_id = kwargs.get("pk")
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            serializer = JobSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                job = serializer.save()
                job.tags.clear()
                tags = request.data.get("tags", [])
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    job.tags.add(tag)
                return Response({"status": "Job updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            return Response({"error": "Job does not exist"}, status=status.HTTP_404_NOT_FOUND)

class ApplicantsListView(APIView):
    permission_classes = [IsAuthenticatedAndVerified, IsEmployer]

    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='applicants_list', method='GET', user=request.user.username).inc()

        status_param = request.GET.get("status")
        queryset = Applicant.objects.filter(job__user=request.user).order_by("id")
        if status_param:
            queryset = queryset.filter(status=status_param)
        serializer = ApplicantSerializer(queryset, many=True)
        return Response({"applicants": serializer.data})

class JobView(APIView):
    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='home', method='GET', user='anonymous').inc()

        jobs = Job.objects.filter(filled=False).order_by("-created_at")
        serializer = JobSerializer(jobs, many=True)
        return Response({"jobs": serializer.data})

class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='search', method='GET', user='anonymous').inc()

        query = request.GET.get("q", "")
        jobs = Job.objects.filter(title__icontains=query, filled=False).order_by("-created_at")
        serializer = JobSerializer(jobs, many=True)
        return Response({"jobs": serializer.data})

class JobListView(APIView):
    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='job_list', method='GET', user='anonymous').inc()

        jobs = Job.objects.filter(filled=False).order_by("-created_at")
        serializer = JobSerializer(jobs, many=True)
        return Response({"jobs": serializer.data})

class JobDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='job_details', method='GET', user='anonymous').inc()

        job_id = kwargs.get("pk")
        try:
            job = Job.objects.get(id=job_id)
            if job.filled:
                return Response({"error": "Job is filled."}, status=status.HTTP_404_NOT_FOUND)
            serializer = JobSerializer(job)
            return Response({"job": serializer.data})
        except Job.DoesNotExist:
            return Response({"error": "Job does not exist"}, status=status.HTTP_404_NOT_FOUND)

class ApplyJobView(APIView):
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, *args, **kwargs):
        # Increment metrics
        requests_total.labels(endpoint='apply_job', method='POST', user=request.user.username).inc()

        job_id = kwargs.get("job_id")
        serializer = ApplyJobSerializer(data=request.data)
        if serializer.is_valid():
            try:
                job = Job.objects.get(id=job_id)
                if job.filled:
                    return Response({"error": "Job is already filled."}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(user=request.user, job=job)
                return Response({"status": "Application submitted successfully"})
            except Job.DoesNotExist:
                return Response({"error": "Job does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
