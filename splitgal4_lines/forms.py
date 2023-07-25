from django import forms
from django.forms import ModelForm
from .models import fly_line

# Create a form for uploading individual lines
class NewLineForm(ModelForm):
    gene_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter the gene symbol',
            }
        )
    )

    effector_type = forms.CharField(
        max_length=3,
        widget=forms.Select(
            choices=fly_line.EFFECTORS,
            attrs={
                'class': 'form-control'
            }
        )
    )

    activator_type = forms.CharField(
        max_length=6,
        widget=forms.Select(
            choices=fly_line.ACTIVATORS,
            attrs={
                'class': 'form-control'
            }
        )
    )
    source_id = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'If this line is from a MiMIC/CRIMIC line, please provide its ID (CR/MI)',
            }
        ),
        required=False
    )
    cassette = forms.CharField(
        max_length=8,
        widget=forms.Select(
            choices=fly_line.CASSETTE_STYLE,
            attrs={
                'class': 'form-control'
            }
        )
    )
    dimerizer = forms.CharField(
        max_length=8,
        widget=forms.Select(
            choices=fly_line.DIMERIZER_STYLE,
            attrs={
                'class': 'form-control'
            }
        )
    )
    ins_seqname = forms.CharField(
        label='Inserted chromosome',
        max_length=8,
        widget=forms.Select(
            choices=fly_line.CHRS,
            attrs={
                'class': 'form-control'
            }
        )
    )
    ins_site = forms.IntegerField(
        label='Insertion coordinate',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=False
    )
    contributor = forms.CharField(
        label='Contributor (e.g., the host lab)',
        max_length=256,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    uploader = forms.CharField(
        widget=forms.HiddenInput()
    )

    reference = forms.CharField(
        max_length=1024,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please provide the citation information if available'
            }
        ),
        required=False
    )
    status = forms.CharField(
        max_length=4,
        widget=forms.Select(
            choices=fly_line.STATUS_LIST,
            attrs={
                'class': 'form-control'
            }
        )
    )
    internal_sharing = forms.BooleanField(required=False)

    class Meta:
        model = fly_line
        fields = (
            'gene_name', 'effector_type', 'activator_type', 'source_id',
            'cassette', 'dimerizer', 'ins_seqname', 'ins_site', 'contributor',
            'uploader', 'reference', 'status', 'internal_sharing'
        )