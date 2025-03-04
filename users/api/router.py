from django.urls import path
from users.api.views import RegisterView, PasswordResetConfirmView, PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    # path('auth/login/', LoginView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    # path('auth/me/', UserView.as_view()),
    path('password-reset/', PasswordResetView.as_view(),
         name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
