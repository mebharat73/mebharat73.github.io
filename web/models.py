from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='profile_pictures/', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.user.username + "'s profile"

#.......................................................................................................................................


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Category"

   
    

 #.......................................................................................................................................   

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    
#........................................................................................................................................    


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

#.........................................................................................................................................    
   



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Like"
        unique_together = ('user', 'post'), ('user', 'comment')

#...........................................................................................................................................
