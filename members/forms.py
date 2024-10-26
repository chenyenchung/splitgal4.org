from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.forms import ModelForm
from .models import CustomUser
from turnstile.fields import TurnstileField

User = CustomUser
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your email',
            }
        )
    )

    first_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your first name',
            }
        )
    )
    last_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your last name',
            }
        )
    )

    affiliation = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your affiliation (optional)',
            }
        ),
        required=False
    )

    lab = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your lab (optional)',
            }
        ),
        required=False
    )

    turnstile = TurnstileField()

    class Meta:
        model = User
        fields = (
            'username', 'first_name', "last_name",
            'email', 'password1', 'password2',
            'affiliation', 'lab'
        )

    # Ensure unique email
    # https://stackoverflow.com/questions/53461410/make-user-email-unique-django
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            self.add_error("email", ValidationError(
                "This email has been used to register an account.", code = "Email"
                ))
       return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your email',
            }
        )
    )

    first_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your first name',
            }
        )
    )
    last_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your last name',
            }
        )
    )

    affiliation = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your affiliation (optional)',
            }
        ),
        required=False
    )

    lab = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your lab (optional)',
            }
        ),
        required=False
        )
    
    class Meta:
        model = User
        fields = (
            'first_name', "last_name",
            'email', 'affiliation', 'lab'
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        

    # Ensure unique email
    # https://stackoverflow.com/questions/53461410/make-user-email-unique-django
    def clean(self):
        init_email = self.initial["email"]
        email = self.cleaned_data.get('email')

        if email != init_email and User.objects.filter(email=email).exists():
            self.add_error("email", ValidationError(
                "This email has been used to register an account.", code = "Email"
                ))
        return self.cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


class EmailPasswordResetForm(ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your email',
            }
        )
    )

    turnstile = TurnstileField()
    
    class Meta:
        model = User
        fields = (
            'email',
        )
