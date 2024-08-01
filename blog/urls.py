from django.urls import path
from .views import (
    BlogListView, BlogDetailView, MyBlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView,
    CommentListView, CommentCreateView, CommentDeleteView, AddLikeView, RemoveLikeView
)

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/my/', MyBlogListView.as_view(), name='my-blogs'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('blogs/<int:blog_pk>/comments/', CommentListView.as_view(), name='comment-list'),
    path('blogs/<int:blog_pk>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('blogs/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('blogs/<int:pk>/like/', AddLikeView.as_view(), name='add-like'),
    path('blogs/<int:pk>/unlike/', RemoveLikeView.as_view(), name='remove-like'),
]
