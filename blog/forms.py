from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'text', 'sourcecode','image', 'height_field', 'width_field')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author','text',)
