from django import forms
from django.core.exceptions import ValidationError
import requests
from django.conf import settings
from .models import BlogPost  # Importa el modelo BlogPost

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, required=True)
    last_name = forms.CharField(label='Your Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Your Email Address', required=True)
    phone = forms.CharField(label='Phone (optional)', max_length=15, required=False)
    message = forms.CharField(label='Your Message', widget=forms.Textarea, required=True)
    recaptcha = forms.CharField(widget=forms.HiddenInput, required=True)  # ReCAPTCHA response

    def clean(self):
        cleaned_data = super().clean()
        recaptcha_response = cleaned_data.get('recaptcha')

        if not recaptcha_response:
            raise ValidationError("ReCAPTCHA validation failed. Please try again.")

        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if not result.get('success'):
            raise ValidationError("Invalid reCAPTCHA. Please try again.")

        return cleaned_data

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image'] 
