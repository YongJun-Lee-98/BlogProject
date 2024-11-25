from django.db import models
import hashlib

# Create your models here.
class User(models.Model):
    idx = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30, unique=True)
    blog_name = models.CharField(max_length=50)
    password = models.CharField(max_length=256) # SHA256 암호화된 비밀번호
    salt = models.CharField(max_length=32, blank=True)
    slug = models.SlugField(unique=True)
    info = models.CharField(max_length=100, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.salt:
            # 랜덤한 salt 생성
            self.salt = hashlib.sha256(self.user_id.encode().hexdigest()[:32])
        if not self.password.startswith('sha256:'):
            # 비밀번호 암호화
            salted_password = self.password + self.salt
            self.password = 'sha256: ' + hashlib.sha256(salted_password.encode().hexdigest())
        super().save(*args, **kwargs)
    def __str__(self):
        return self.blog_name

class Post(models.Model):
    user_idx = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

class Category(models.Model):
    user_idx = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="subcategories")
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('user_idx', 'slug')

class Tag(models.Model):
    user_idx = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag")
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('user_idx', 'slug')

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="posts")