from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='profile_pictures/', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username + "'s profile"

#..................................................................................................
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment") 

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    class Meta:
        unique_together = ('post', 'user') 

class Posttag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="posts")
