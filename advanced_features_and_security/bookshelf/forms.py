from django import forms
from .models import YourModelName  # Replace with your actual model name

class YourModelForm(forms.ModelForm):
    class Meta:
        model = YourModelName  # Replace with your actual model name
        fields = ['field1', 'field2', 'field3']  # Replace with your actual fields
        widgets = {
            'field1': forms.TextInput(attrs={'class': 'form-control'}),
            'field2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'field3': forms.FileInput(attrs={'class': 'form-control'}),
        }