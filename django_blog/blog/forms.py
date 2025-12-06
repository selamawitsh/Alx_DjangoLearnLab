from django import forms
from .models import Comment, Post, Tag

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
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (e.g., python, django, webdev)"
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()

        # Handle tags
        tags_str = self.cleaned_data.get("tags", "")
        tag_names = [t.strip().lower() for t in tags_str.split(",") if t.strip()]

        tag_objects = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_objects.append(tag)

        post.tags.set(tag_objects)
        return post
