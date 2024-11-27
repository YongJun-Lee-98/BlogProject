from django.urls import path
from .views import create_post
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('add-post/', create_post, name='create_post'),
    path('api-token-access/', obtain_auth_token),
]