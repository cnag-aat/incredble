from django import forms
from resistome.models import GenomeUpload

class GenomeUploadForm(forms.ModelForm):
    class Meta:
        model = GenomeUpload
        fields = ('description', 'fasta', )
