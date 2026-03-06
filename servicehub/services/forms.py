from django import forms

FEEDBACK_TYPES = [
    ('', 'Select a topic'),
    ('complaint', '⚠️ Complaint about a provider'),
    ('bug', '🐛 Report a bug / issue'),
    ('suggestion', '💡 Feature suggestion'),
    ('general', '💬 General feedback'),
]


class FeedbackForm(forms.Form):
    """Customer → Admin feedback / complaint form."""

    feedback_type = forms.ChoiceField(
        choices=FEEDBACK_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Topic',
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brief summary of your issue',
        }),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your issue or feedback in detail...',
            'rows': 6,
        }),
    )


RATING_CHOICES = [(i, f'{i} ★') for i in range(1, 6)]


class ReviewForm(forms.Form):
    """Customer review form for rating a service provider."""

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Rating',
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Share your experience (optional)...',
            'rows': 4,
        }),
        label='Your Review',
    )
