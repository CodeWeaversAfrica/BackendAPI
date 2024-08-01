from django.urls import path
from .views import (
    PostListView, PostDetailView, MyPostListView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentListView, CommentCreateView, CommentDeleteView, AddLikeView, RemoveLikeView
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/my/', MyPostListView.as_view(), name='my-posts'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:post_pk>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<int:post_pk>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('posts/<int:pk>/like/', AddLikeView.as_view(), name='add-like'),
    path('posts/<int:pk>/unlike/', RemoveLikeView.as_view(), name='remove-like'),
]
