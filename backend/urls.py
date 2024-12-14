from django.urls import path
from .views import UserLoginView, TokenObtainPairView, UserRegistrationSerializer, UserRegistrationView, TokenRefreshView

urlpatterns = [
    # path('/', , name='token_obtain_pair'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='toekn-refresh'),
]