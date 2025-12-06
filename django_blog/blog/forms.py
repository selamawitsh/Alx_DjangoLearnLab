# blog/forms.py
from django import forms
from .models import Comment, Post
from taggit.forms import TagWidget

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'form-control'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment is too long (max 2000 characters).")
        return content

# Post form with tags
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            'tags': TagWidget(),  # Proper tag widget from django-taggit
        }
