from .models import Post, Comment
from django import forms 
from .models import Category
from .models import CommentReply
from web.models import BlogImage  # Ensure this import is correct
from django import forms
from .models import Profile



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"



from django import forms
from .models import Post  # Make sure to import your Post model

class CreateBlogForm(forms.ModelForm):
    # Replace SummernoteWidget with a standard Textarea widget
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 70}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
                  
    def save(self, commit=True, **kwargs):
        blog = super().save(commit=False)
        blog.author = kwargs.get('author')
        if commit:
            blog.save()
        return blog
    

from django import forms
from .models import Post, BlogImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']  # Include other fields as necessary

class PostImageForm(forms.ModelForm):
    class Meta:
        model = BlogImage
        fields = ['image']  # Only the image field

        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']

    def save(self, commit=True, **kwargs):
        comment = super().save(commit=False)
        comment.author = kwargs.get('commenter')
        comment.post = kwargs.get('post')
        if commit:
            comment.save()
        return comment





class CommentReplyForm(forms.ModelForm):
    
    class Meta:
        model = CommentReply
        fields = ['content']

    def save(self, commit=True, **kwargs):
        reply = super().save(commit=False)
        reply.author = kwargs.get('replier')
        reply.comment = kwargs.get('comment')
        if commit:
            reply.save()
        return reply
    