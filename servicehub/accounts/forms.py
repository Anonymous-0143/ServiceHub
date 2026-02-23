from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from services.models import Category, ProviderProfile


class CustomerRegistrationForm(UserCreationForm):
    """Registration form for customers — basic account fields only."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user


class ProviderRegistrationForm(UserCreationForm):
    """Registration form for service providers — includes provider profile fields."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Select a service category',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    experience = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Years of experience',
        }),
        label='Experience (years)',
    )
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your city or area',
        }),
    )
    hourly_rate = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 500.00',
        }),
        label='Hourly Rate (₹)',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ('category',):
                self.fields[field].widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'provider'
        if commit:
            user.save()
            ProviderProfile.objects.create(
                user=user,
                category=self.cleaned_data['category'],
                experience=self.cleaned_data['experience'],
                location=self.cleaned_data['location'],
                hourly_rate=self.cleaned_data['hourly_rate'],
            )
        return user


class ProfileForm(forms.ModelForm):
    """Form for editing basic user details (both customers & providers)."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }


class ProviderProfileForm(forms.ModelForm):
    """Form for editing provider-specific details."""

    class Meta:
        model = ProviderProfile
        fields = ('category', 'experience', 'location', 'hourly_rate')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city or area'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500.00'}),
        }
        labels = {
            'experience': 'Experience (years)',
            'hourly_rate': 'Hourly Rate (₹)',
        }
