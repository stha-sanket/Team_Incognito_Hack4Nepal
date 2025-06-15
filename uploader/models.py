from django.db import models

# Create your models here.

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis_result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"

class RPAScript(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    script_file = models.FileField(upload_to='rpa_scripts/')
    data_file = models.FileField(upload_to='rpa_scripts/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_run = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
