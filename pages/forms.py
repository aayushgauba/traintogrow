from django import forms
from .models import CourseFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = CourseFile
        fields = ['title', 'description', 'file']
