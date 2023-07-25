from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

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
    


    class Meta:
        model = User
        fields = (
            'username', 'first_name', "last_name",
            'email', 'password1', 'password2',
            'affiliation', 'lab'
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")