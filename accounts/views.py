import http
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, views, permissions

from accounts.renderers import UserRenderer
from .api.serializer import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, MyTokenObtainPairSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.getenv('APP_SCHEME', 'http')]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        frontend_url =  os.getenv('FRONTEND_URL')
        absurl = f'{frontend_url}/verify-email?token={str(token)}'
        email_body = 'Hi ' + user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email'
        }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Token for email verification', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token', None)
        if not token:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id')
            user = get_object_or_404(User, id=user_id)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                # Set this in your environment variables
            frontend_url = os.getenv('FRONTEND_URL')
            redirect_url = f'{frontend_url}/verify-email'
            return CustomRedirect(redirect_url)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
