from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Feedback

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Register As'
    )

class FeedbackForm(forms.ModelForm):
    FOOD_CHOICES = [
        ('Breakfast', 'Breakfast (Idli, Dosa, Chutney)'),
        ('Lunch', 'Lunch (Rice, Dal, Curry)'),
        ('Dinner', 'Dinner (Chapati, Curry)'),
    ]
    
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ (5 - Excellent)'),
        (4, '⭐⭐⭐⭐ (4 - Good)'),
        (3, '⭐⭐⭐ (3 - Average)'),
        (2, '⭐⭐ (2 - Poor)'),
        (1, '⭐ (1 - Very Poor)'),
    ]

    food_item = forms.ChoiceField(
        choices=FOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Feedback
        fields = ['food_item', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }