from django import forms
from django.forms import ModelForm
from .models import fly_line

class RemoveLineForm(ModelForm):
  removed = forms.BooleanField(
    required=False,
    widget=forms.HiddenInput()
  )
  class Meta:
    model = fly_line
    fields = ('removed',)
