from django import forms
from .models import Book  # Replace with your actual model name

class BookForm(forms.ModelForm):
    class Meta:
        model = Book  # Replace with your actual model name
        fields = ['title', 'author']  # Replace with your actual fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }