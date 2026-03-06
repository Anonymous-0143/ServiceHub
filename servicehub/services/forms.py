from django import forms

FEEDBACK_TYPES = [
    ('', 'Select a topic'),
    ('complaint', '⚠️ Complaint about a provider'),
    ('bug', '🐛 Report a bug / issue'),
    ('suggestion', '💡 Feature suggestion'),
    ('general', '💬 General feedback'),
]


class FeedbackForm(forms.Form):
    """Customer & Provider feedback / complaint form."""

    feedback_type = forms.ChoiceField(
        choices=[],  # Set dynamically in __init__
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        provider_choices = [
            ('', 'Select a topic'),
            ('customer_issue', '⚠️ Issue with a customer'),
            ('payment_issue', '💸 Payment or listing issue'),
            ('bug', '🐛 Report a platform bug'),
            ('suggestion', '💡 Feature suggestion'),
            ('general', '💬 General feedback'),
        ]
        
        customer_choices = [
            ('', 'Select a topic'),
            ('complaint', '⚠️ Complaint about a provider'),
            ('bug', '🐛 Report a bug / issue'),
            ('suggestion', '💡 Feature suggestion'),
            ('general', '💬 General feedback'),
        ]

        if user and hasattr(user, 'role') and user.role == 'provider':
            self.fields['feedback_type'].choices = provider_choices
        else:
            self.fields['feedback_type'].choices = customer_choices


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
