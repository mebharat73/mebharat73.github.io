from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey








class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pictures/', default='default_profile_picture.jpg')

    def __str__(self):
        return f"{self.user.username}'s profile"

#.......................................................................................................................................


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Category"
    def __str__(self):
        return self.name

   
    

 #.......................................................................................................................................   

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    #likes_count = models.IntegerField(default=0)
    @property
    def likes_count(self):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).count()
    
#........................................................................................................................................    


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    #likes_count = models.IntegerField(default=0)
    @property
    def likes_count(self):
        return Like.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).count()
    
    
#.........................................................................................................................................    




class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
    def __str__(self):
        return self.content_type
#...........................................................................................................................................

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)