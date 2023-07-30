from django import forms
from django.forms import ModelForm
from django.conf import settings
from splitgal4_lines.models import fly_line
from members.models import CustomUser

TEMPLATE = settings.TEMPLATE

class UploadFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control form-control-sm',
            }
        )
    )

# Create a form for uploading individual lines
class NewLineForm(ModelForm):
    gene_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter the gene symbol',
            }
        ),
        required = True
    )

    effector_type = forms.CharField(
        widget=forms.Select(
            choices=TEMPLATE.field_opts['effector_type'],
            attrs={
                'class': 'form-control',
            }
        )
    )

    source_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'If this line is from a MiMIC/CRIMIC line, please provide its ID (e.g., CR12345 or MI54321)',
            }
        ),
        required=False
    )
    cassette = forms.CharField(
        widget=forms.Select(
            choices=TEMPLATE.field_opts['cassette'],
            attrs={
                'class': 'form-control',
            }
        )
    )
    dimerizer = forms.CharField(
        widget=forms.Select(
            choices=TEMPLATE.field_opts['dimerizer'],
            attrs={
                'class': 'form-control'
            }
        )
    )
    ins_seqname = forms.CharField(
        label='Inserted chromosome',
        widget=forms.Select(
            choices=TEMPLATE.field_opts['ins_seqname'],
            attrs={
                'class': 'form-control'
            }
        )
    )
    ins_site = forms.IntegerField(
        label='Insertion coordinate (if known)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=False
    )
    contributor = forms.CharField(
        label='Contributor (e.g., the host lab)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    uploader = forms.ModelChoiceField(
        queryset = CustomUser.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    citation = forms.CharField(
        label='Citation info (Optional; PMID is preferred)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please provide the citation information if available'
            }
        ),
        required=False
    )
    status = forms.CharField(
        widget=forms.Select(
            choices=TEMPLATE.field_opts['status'],
            attrs={
                'class': 'form-control'
            }
        )
    )
    contact = forms.EmailField(
        label='Contact email (for reagent requests)',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    notes = forms.CharField(
        max_length=2048,
        required=False,
        label='Notes',
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Other information that you want to share with others',
            }
        )
    )

    private = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = fly_line
        fields = (
            'gene_name', 'effector_type', 'source_id',
            'cassette', 'dimerizer', 'ins_seqname', 'ins_site', 'contributor',
            'uploader', 'citation', 'status', 'contact', 'notes', 'private'
        )

class AnonNewLineForm(NewLineForm):
    class Meta:
        model = fly_line
        fields = (
            'gene_name', 'effector_type', 'source_id',
            'cassette', 'dimerizer', 'ins_seqname', 'ins_site', 'contributor',
            'citation', 'status', 'contact', 'notes', 'private'
        )