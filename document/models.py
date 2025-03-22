from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="documents/")  # Uploads to MEDIA_ROOT/documents/
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Prompt(models.Model):
    text = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)