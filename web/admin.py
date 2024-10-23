from django.contrib import admin
from .models import Profile, Post, Comment, Like, Category, CommentReply, Message, Room
from django.contrib.auth.models import User

class ProfileInline(admin.TabularInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
    ]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register (Profile)
admin.site.register (Post)
admin.site.register (Comment)
admin.site.register (Like)
admin.site.register (Category)
admin.site.register (CommentReply)
admin.site.register (Message)
admin.site.register(Room)










# Register your models here.
