from django.urls import path
from .views import (
    QuestionListView, QuestionDetailView, AnswerListView, AnswerDetailView, VoteCreateView,
    CommentListView, CommentDetailView
)

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:question_pk>/answers/', AnswerListView.as_view(), name='answer-list'),
    path('questions/<int:question_pk>/answers/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('answers/<int:answer_pk>/votes/', VoteCreateView.as_view(), name='vote-create'),
    path('answers/<int:answer_pk>/comments/', CommentListView.as_view(), name='comment-list'),
    path('answers/<int:answer_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
