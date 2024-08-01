from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied 
from accounts.permissions import IsAuthenticatedAndVerified
from .permissions import IsAdminOrModerator, IsAuthor, IsCommentAuthor
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer, CommentCreateSerializer

class BlogListView(generics.ListAPIView):
    """
    List all blogs or filter by category.
    """
    serializer_class = BlogSerializer

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        if category:
            return Blog.objects.filter(category__name=category)
        return Blog.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

class BlogDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single blog.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class MyBlogListView(generics.ListAPIView):
    """
    List all blogs created by the authenticated user.
    """
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

class BlogCreateView(generics.CreateAPIView):
    """
    Create a new blog.
    """
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogUpdateView(generics.UpdateAPIView):
    """
    Update an existing blog.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator, IsAuthor ]

    def perform_update(self, serializer):
        blog = self.get_object()
        user = self.request.user
        
        # Check if the user is an admin or moderator
        if user.is_staff or user.is_superuser:
            # Admins and moderators can update any blog
            serializer.save()
        else:
            # If not an admin or moderator, ensure they are the author
            if blog.author == user:
                serializer.save()
            else:
                raise PermissionDenied('Not authorized to edit this blog')

class BlogDeleteView(generics.DestroyAPIView):
    """
    Delete a blog.
    """
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator, IsAuthor ]

    def perform_destroy(self, instance):
        user = self.request.user
        
        # Check if the user is an admin or moderator
        if user.is_staff or user.is_superuser:
            # Admins and moderators can delete any blog
            instance.delete()
        else:
            # If not an admin or moderator, ensure they are the author
            if instance.author == user:
                instance.delete()
            else:
                raise PermissionDenied('Not authorized to delete this blog')

class CommentListView(generics.ListAPIView):
    """
    List all comments for a blog.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(blog=self.kwargs['blog_pk'])

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
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator, IsCommentAuthor]

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
    Add a like to a blog.
    """
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, pk, *args, **kwargs):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({'detail': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in blog.likes.all():
            return Response({'detail': 'Blog already liked'}, status=status.HTTP_400_BAD_REQUEST)

        blog.likes.add(request.user)
        blog.save()
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data)

class RemoveLikeView(generics.GenericAPIView):
    """
    Remove a like from a blog.
    """
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, pk, *args, **kwargs):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({'detail': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in blog.likes.all():
            return Response({'detail': 'Blog not liked yet'}, status=status.HTTP_400_BAD_REQUEST)

        blog.likes.remove(request.user)
        blog.save()
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data)
