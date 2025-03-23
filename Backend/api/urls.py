from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from userauth.views import (
    MyTokenObtainPairView,
    RegisterView,
    PasswordEmailVerify,
    PasswordChangeView,
    UserProfileView
)

app_name = 'userauth'

urlpatterns = [
    # Authentication endpoints
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Password reset flow
    path('password-reset-email/<str:email>/', PasswordEmailVerify.as_view(), name='password_reset_email'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    
    # User profile management
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]