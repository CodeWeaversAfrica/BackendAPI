from django.urls import path
from .views import (
    EmployeeMyJobsListView,
    EditProfileView,
    FavoriteListView,
    DashboardView,
    ApplicantPerJobView,
    JobCreateView,
    JobUpdateView,
    ApplicantsListView,
    JobView,
    SearchView,
    JobListView,
    JobDetailsView,
    ApplyJobView,
)

app_name = 'jobs'

urlpatterns = [
    path('my-jobs/', EmployeeMyJobsListView.as_view(), name='employee-my-jobs'),
    # Profile Views - should be in the profiles app
    #path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('job/<int:job_id>/applicants/', ApplicantPerJobView.as_view(), name='applicant-per-job'),
    path('applicants/', ApplicantsListView.as_view(), name='applicants-list'),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/search/', SearchView.as_view(), name='search-jobs'),
    path('jobs/<int:pk>/', JobDetailsView.as_view(), name='job-details'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('jobs/<int:job_id>/apply/', ApplyJobView.as_view(), name='apply-job'),
]
