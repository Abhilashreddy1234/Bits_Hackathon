from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["file"]
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["title", "description", "date"]
