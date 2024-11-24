# admin.py

from django.contrib import admin
from .models import Room, Message, Profile, Category, Post, Comment, Like, CommentReply, BlogImage    # Import your models here

# Register your models here
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentReply)
admin.site.register(BlogImage)

