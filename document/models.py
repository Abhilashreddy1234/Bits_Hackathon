from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="documents/")  # Uploads to MEDIA_ROOT/documents/
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Prompt(models.Model):
    text = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.models import User

class Case(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
