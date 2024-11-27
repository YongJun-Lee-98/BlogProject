from rest_framework import serializers
from .models import User, Post, Category, Tag, PostTag, TestPostModule

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         field = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPostModule
        fields = '__all__'

