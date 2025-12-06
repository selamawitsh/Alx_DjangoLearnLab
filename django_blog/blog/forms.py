# blog/forms.py
from django import forms
from .models import Comment

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

        # Check empty comment
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")

        # Check length
        if len(content) > 2000:
            raise forms.ValidationError("Comment is too long (max 2000 characters).")

        return content
