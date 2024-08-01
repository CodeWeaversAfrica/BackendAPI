from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from accounts.permissions import IsAuthenticatedAndVerified
from django.shortcuts import get_object_or_404
from .models import Question, Answer, Vote, Comment
from .permissions import IsAdminOrModerator, IsAnswerAuthor, IsQuestionAuthor, IsCommentAuthor
from .serializers import QuestionSerializer, AnswerSerializer, VoteSerializer, CommentSerializer

class QuestionListView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        if category:
            return Question.objects.filter(category__name=category)
        return Question.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator, IsQuestionAuthor]

    def perform_update(self, serializer):
        question = self.get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or question.author == user:
            serializer.save()
        else:
            raise PermissionDenied('You are not allowed to edit this question.')

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_staff or user.is_superuser or instance.author == user:
            instance.delete()
        else:
            raise PermissionDenied('You are not allowed to delete this question.')

class AnswerListView(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        question = self.kwargs['question_pk']
        return Answer.objects.filter(question_id=question)

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_pk'])
        serializer.save(author=self.request.user, question=question)

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsAdminOrModerator, IsAnswerAuthor]

    def perform_update(self, serializer):
        answer = self.get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or answer.author == user:
            serializer.save()
        else:
            raise PermissionDenied('You are not allowed to edit this answer.')

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_staff or user.is_superuser or instance.author == user:
            instance.delete()
        else:
            raise PermissionDenied('You are not allowed to delete this answer.')

class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def perform_create(self, serializer):
        answer = get_object_or_404(Answer, pk=self.kwargs['answer_pk'])
        user = self.request.user
        value = serializer.validated_data['value']

        if value not in [1, -1]:
            return Response({'detail': 'Invalid vote value. Must be 1 for upvote or -1 for downvote.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already voted on this answer
        existing_vote = Vote.objects.filter(user=user, answer=answer).first()
        if existing_vote:
            if existing_vote.value == value:
                return Response({'detail': 'You have already cast this vote.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                existing_vote.value = value
                existing_vote.save()
                return Response(VoteSerializer(existing_vote).data, status=status.HTTP_200_OK)

        # Create a new vote if none exists
        serializer.save(user=user, answer=answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_queryset(self):
        answer = self.kwargs['answer_pk']
        return Comment.objects.filter(answer_id=answer)

    def perform_create(self, serializer):
        answer = get_object_or_404(Answer, pk=self.kwargs['answer_pk'])
        serializer.save(author=self.request.user, answer=answer)

class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAndVerified, IsCommentAuthor, IsAdminOrModerator]

    def perform_update(self, serializer):
        comment = self.get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or comment.author == user:
            serializer.save()
        else:
            raise PermissionDenied('You are not allowed to edit this comment.')

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_staff or user.is_superuser or instance.author == user:
            instance.delete()
        else:
            raise PermissionDenied('You are not allowed to delete this comment.')