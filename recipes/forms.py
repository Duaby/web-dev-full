from django import forms
from .models import Subscriber, Review, ContactMessage

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'required': True
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label="Rating"
    )

    class Meta:
        model = Review
        fields = ['recipe', 'reviewer_name', 'reviewer_email', 'rating', 'comment']
        widgets = {
            'recipe': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'reviewer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
                'required': True
            }),
            'reviewer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about this recipe...',
                'rows': 4,
                'required': True
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message...',
                'rows': 6,
                'required': True
            }),
        }
