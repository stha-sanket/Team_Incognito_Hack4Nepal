from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

class Application(models.Model):
    TYPE_CHOICES = [
        ('citizenship', 'Citizenship'),
        ('pan', 'PAN Card'),
        ('contact', 'Contact'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Base fields
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    created_at = models.DateTimeField(default=timezone.now)
    
    # Common fields for both Citizenship and PAN
    country = models.CharField(max_length=100, default='Nepal')
    full_name = models.CharField(max_length=200)
    sex = models.CharField(max_length=10)
    
    # Date of Birth fields
    birth_year = models.IntegerField(null=True)
    birth_month = models.CharField(max_length=3, null=True)  # JAN, FEB, etc.
    birth_day = models.IntegerField(null=True)
    
    # Citizenship specific fields
    citizenship_certificate_number = models.CharField(max_length=100, blank=True)
    birth_district = models.CharField(max_length=100, blank=True)
    birth_municipality = models.CharField(max_length=100, blank=True)
    birth_ward_no = models.IntegerField(null=True, blank=True)
    permanent_district = models.CharField(max_length=100, blank=True)
    permanent_municipality = models.CharField(max_length=100, blank=True)
    permanent_ward_no = models.IntegerField(null=True, blank=True)
    issuing_officer_name = models.CharField(max_length=200, blank=True)
    issuing_officer_title = models.CharField(max_length=200, blank=True)
    issuing_date_bs = models.CharField(max_length=50, blank=True)
    
    # PAN specific fields
    pan_number = models.CharField(max_length=100, blank=True)
    
    # Contact specific fields
    message = models.TextField(blank=True)
    
    # Image path
    image_path = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.type} - {self.user.email} - {self.status}"

    class Meta:
        ordering = ['-created_at']
