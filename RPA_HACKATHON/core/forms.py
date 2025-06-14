from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import User, Application

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address']

class CitizenshipApplicationForm(forms.ModelForm):
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    MONTH_CHOICES = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    ]
    
    full_name = forms.CharField(max_length=200)
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    birth_year = forms.IntegerField(
        validators=[
            MinValueValidator(1900, message="Year must be 1900 or later"),
            MaxValueValidator(2024, message="Year cannot be in the future")
        ]
    )
    birth_month = forms.ChoiceField(choices=MONTH_CHOICES)
    birth_day = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Day must be between 1 and 31"),
            MaxValueValidator(31, message="Day must be between 1 and 31")
        ]
    )
    
    class Meta:
        model = Application
        fields = [
            'full_name',
            'sex',
            'birth_year',
            'birth_month',
            'birth_day',
        ]
        
    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation here if needed
        return cleaned_data

class PANApplicationForm(forms.ModelForm):
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    MONTH_CHOICES = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    ]
    
    full_name = forms.CharField(max_length=200)
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    birth_year = forms.IntegerField(
        validators=[
            MinValueValidator(1900, message="Year must be 1900 or later"),
            MaxValueValidator(2024, message="Year cannot be in the future")
        ]
    )
    birth_month = forms.ChoiceField(choices=MONTH_CHOICES)
    birth_day = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Day must be between 1 and 31"),
            MaxValueValidator(31, message="Day must be between 1 and 31")
        ]
    )
    
    class Meta:
        model = Application
        fields = [
            'full_name',
            'sex',
            'birth_year',
            'birth_month',
            'birth_day',
        ]
        
    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation here if needed
        return cleaned_data

class ContactForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Application
        fields = ['message']
        
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Message is required")
        return message 