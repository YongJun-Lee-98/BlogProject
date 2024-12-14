from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(TokenObtainPairView):
    # 기본적인 TokenObtainPairView를 사용하면 됨
    pass

class TokenRefreshView(TokenRefreshView):
    # 기본적인 TokenRefreshView를 사용하여 토큰을 갱신할 수 있음
    pass

