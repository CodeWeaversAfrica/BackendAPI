from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterView, VerifyEmail, MyTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uuid:short_id>/', VerifyEmail.as_view(), name='verify-email'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('request-reset-email/', RequestPasswordResetEmail.as_view(),
    #      name='request-reset-email'),
    # path('password-reset/<uidb64>/<token>/',
    #      PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
    #      name='password-reset-complete'),
    # path('logout/', LogoutAPIView.as_view(), name='logout'),
]