# django
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

import hashlib

"""
Django의 기본 auth_user 테이블은
AbstractUser 또는 AbstractBaseUser 클래스를 기반으로 동작합니다.
이를 확장하면 기존 auth_user의 기본 구조와 호환되면서 커스텀 필드를 추가할 수 있습니다.
Django의 기본 사용자 모델을 확장하여 
auth_user에 필요한 필드(salt, slug, info, blog_name)를 추가하는 방법입니다.

확장한 방법에서도 문제가 발생하였음

"""

"""
- 오류 정리
backend.CustomUser.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'backend.CustomUser.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'.
HINT: Add or change a related_name argument to the definition for 'backend.CustomUser.user_permissions' or 'auth.User.user_permissions'.

해당 오류는 CustomUser 모델이 Django 기본 User 모델을 확장하는 과정에서
groups와 user_permissions 필드의 기본 reverse accessor가 충돌하여 발생합니다.
이를 해결하려면 CustomUser 모델의 groups와 user_permissions 필드에
related_name 속성을 명시적으로 설정해야 합니다.
- 해결방안
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # 기본 'user_set' 대신 변경
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # 기본 'user_set' 대신 변경
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
"""

class CustomUser(AbstractUser):
    # AbstractUser 필드 외에 추가 필드
    blog_name = models.CharField(max_length=50)
    salt = models.CharField(max_length=32, blank=True)
    info = models.CharField(max_length=100, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # 기본 'user_set' 대신 변경
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # 기본 'user_set' 대신 변경
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        if not self.salt:
            # 랜덤한 salt 생성
            self.salt = hashlib.sha256(self.user_id.encode()).hexdigest()[:32]
        if not self.password.startswith('sha256:'):
            # 비밀번호 암호화
            salted_password = self.password + self.salt
            self.password = 'sha256:' + hashlib.sha256(salted_password.encode()).hexdigest()
        
        super().save(*args, **kwargs)


# class Post(models.Model):
#     user_idx = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     description = models.CharField(max_length=255, blank=True)
#     slug = models.SlugField(unique=True)
    
#     def __str__(self):
#         return self.title

# class Category(models.Model):
#     user_idx = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="subcategories")
#     name = models.CharField(max_length=30)
#     slug = models.SlugField()
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         unique_together = ('user_idx', 'slug')

# class Tag(models.Model):
#     user_idx = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag")
#     name = models.CharField(max_length=50)
#     slug = models.SlugField()
    
#     def __str__(self):
#         return self.name
#     class Meta:
#         unique_together = ('user_idx', 'slug')

# class PostTag(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tags")
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="posts")
    
# class TestPostModule(models.Model):
#     title = models.CharField(max_length=30)
#     author = models.CharField(max_length=30)
#     post = models.CharField(max_length=30)
#     def __str__(self):
#         return self.title