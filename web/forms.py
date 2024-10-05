from .models import Post, Comment
from django import forms 
from .models import Category
from django_summernote.widgets import SummernoteWidget
from .models import CommentReply





class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class CreateBlogForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget(attrs={'height':300, 'width':800}))
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
                  
    def save(self, commit=True, **kwargs):
        
        blog = super().save(commit=False)
        blog.author = kwargs.get('author')
        if commit:
            blog.save()
        return blog
                   

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
    