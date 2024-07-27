from asyncio.log import logger
import http
import logging
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, views, permissions

from accounts.renderers import UserRenderer
from .api.serializer import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, MyTokenObtainPairSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, PendingUser, EmailVerification
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import make_password
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
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        # Check if email exists in User
        if User.objects.filter(email=email).exists():
            return Response({'error': "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email exists in PendingUser and if so, whether the verification link has expired
        try:
            pending_user = PendingUser.objects.get(email=email)
            # If a pending user exists, delete it to allow re-registration
            pending_user.delete()
        except PendingUser.DoesNotExist:
            pass

        # Hash the password
        hashed_password = make_password(password)

        # Create a token for email verification
        token_payload = {'email': email}
        token = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm='HS256')

        # Save the user data to PendingUser
        pending_user = PendingUser.objects.create(
            email=email, username=username, first_name=first_name,
            last_name=last_name, phone_number=phone_number,
            password=hashed_password, token=str(token)
        )

        # Create a short URL for verification
        verification_entry = EmailVerification.objects.create(
            email=email, token=str(token)
        )

        # Send verification email
        relative_link = f'/verify-email/{verification_entry.short_id}/'
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        absurl = f'{frontend_url}{relative_link}'
        email_body = f'Hi {username},\nUse the link below to verify your email:\n{absurl}'
        data = {
            'email_body': email_body,
            'to_email': email,
            'email_subject': 'Verify your email'
        }
        Util.send_email(data)

        return Response({'message': "Verification email sent"}, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    short_id_param_config = openapi.Parameter(
        'short_id', in_=openapi.IN_PATH, description='Short ID for email verification', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[short_id_param_config])
    def get(self, request, short_id=None):
        if not short_id:
            return Response({'error': 'Short ID is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the short_id exists in the EmailVerification model
        try:
            verification_entry = EmailVerification.objects.get(
                short_id=short_id)
            if verification_entry:
                return Response({"message": "Valid verification Link"}, status=status.HTTP_202_ACCEPTED)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

        token = verification_entry.token

        # Decode the token and extract email
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get('email')
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"Unexpected error during token decoding: {str(e)}")
            return Response({'error': 'An error occurred during verification.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure email exists in PendingUser
        try:
            pending_user = get_object_or_404(PendingUser, email=email)
        except Exception as e:
            logging.error(f"No matching pending user found: {str(e)}")
            return Response({'error': 'No matching pending user found.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Move data from PendingUser to User
            user = User.objects.create(
                email=pending_user.email,
                username=pending_user.username,
                first_name=pending_user.first_name,
                last_name=pending_user.last_name,
                phone_number=pending_user.phone_number,
                password=pending_user.password,  # Password is already hashed
                is_verified=True
            )

            # Delete the pending user and verification entry
            pending_user.delete()
            verification_entry.delete()

            return Response({'message': 'Email verified successfully'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logging.error(f"Unexpected error during user creation: {str(e)}")
            return Response({'error': 'An error occurred while verifying the email.'}, status=status.HTTP_400_BAD_REQUEST)
