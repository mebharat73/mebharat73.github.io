from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUser   # Corrected import statement
from .models import Profile, Post, Comment, Like, Category, CommentReply, Message, Room, CustomUser    

User  = get_user_model()

# Unregister the default User model if necessary
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Ignore if not registered

# Define an inline for the Profile model
class ProfileInline(admin.TabularInline):
    model = Profile

# Create a custom UserAdmin class
class UserAdmin(BaseUser ):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

# Register your custom user model with the UserAdmin
admin.site.register(CustomUser , UserAdmin)

# Register other models
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(CommentReply)
admin.site.register(Message)
admin.site.register(Room)