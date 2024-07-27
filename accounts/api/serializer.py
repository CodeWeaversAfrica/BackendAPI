from django.conf import settings
import jwt
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import EmailVerification

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email", "username", "first_name", "last_name", 
            "phone_number", "password", "role"
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            phone_number=validated_data["phone_number"],
            role=validated_data.get("role", User.STUDENT)
        )

        return user

class ShortIdSerializer(serializers.Serializer):
    email = serializers.EmailField()
    short_id = serializers.CharField(max_length=255)

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ['short_id', 'email', 'token']
        extra_kwargs = {
            # Assuming `short_id` is automatically generated
            'short_id': {'read_only': True},
            # Assuming `token` is automatically generated
            'token': {'read_only': True},
        }

    def validate(self, attrs):
        short_id = self.context['short_id']
        try:
            verification_entry = EmailVerification.objects.get(
                short_id=short_id)
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid verification link.")

        token = verification_entry.token
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Activation link expired.")
        except jwt.exceptions.DecodeError:
            raise serializers.ValidationError("Invalid token.")

        return attrs

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid login credentials')
        
        if not user.is_verified:
            raise serializers.ValidationError('Email is not verified')
        
        token = RefreshToken.for_user(user)

        return {
            "email": user.email,
            'access': str(token.access_token),
            "refresh": str(token),
        }
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class SetNewPasswordSerializer(serializers.Serializer):
    pass


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    pass


class LogoutSerializer(serializers.Serializer):
    pass