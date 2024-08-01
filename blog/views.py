from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.exceptions import PermissionDenied 
from accounts.permissions import IsAuthenticatedAndVerified
from .permissions import IsAdminOrModerator, IsAuthor, IsCommentAuthor
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer

class PostListView(generics.ListAPIView):
    """
    List all posts or filter by category.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        if category:
            return Post.objects.filter(category__name=category)
        return Post.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

class PostDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class MyPostListView(generics.ListAPIView):
    """
    List all posts created by the authenticated user.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

class PostCreateView(generics.CreateAPIView):
    """
    Create a new post.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostUpdateView(generics.UpdateAPIView):
    """
    Update an existing post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator,IsAuthor ]

    def perform_update(self, serializer):
        post = self.get_object()
        user = self.request.user
        
        # Check if the user is an admin or moderator
        if user.is_staff or user.is_superuser:
            # Admins and moderators can update any post
            serializer.save()
        else:
            # If not an admin or moderator, ensure they are the author
            if post.author == user:
                serializer.save()
            else:
                raise PermissionDenied('Not authorized to edit this post')

class PostDeleteView(generics.DestroyAPIView):
    """
    Delete a post.
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator,IsAuthor ]

    def perform_destroy(self, instance):
        user = self.request.user
        
        # Check if the user is an admin or moderator
        if user.is_staff or user.is_superuser:
            # Admins and moderators can delete any post
            instance.delete()
        else:
            # If not an admin or moderator, ensure they are the author
            if instance.author == user:
                instance.delete()
            else:
                raise PermissionDenied('Not authorized to delete this post')

class CommentListView(generics.ListAPIView):
    """
    List all comments for a post.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

class CommentCreateView(generics.CreateAPIView):
    """
    Create a new comment.
    """
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDeleteView(generics.DestroyAPIView):
    """
    Delete a comment.
    """
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator,IsCommentAuthor]

    def perform_destroy(self, instance):
        user = self.request.user
        
        # Check if the user is an admin or moderator
        if user.is_staff or user.is_superuser:
            # Admins and moderators can delete any comment
            instance.delete()
        else:
            # If not an admin or moderator, ensure they are the comment author
            if instance.author == user:
                instance.delete()
            else:
                raise PermissionDenied('Not authorized to delete this comment')

class AddLikeView(generics.GenericAPIView):
    """
    Add a like to a post.
    """
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in post.likes.all():
            return Response({'detail': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.add(request.user)
        post.save()
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

class RemoveLikeView(generics.GenericAPIView):
    """
    Remove a like from a post.
    """
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in post.likes.all():
            return Response({'detail': 'Post not liked yet'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.remove(request.user)
        post.save()
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
