from django import forms
from django.core.files import File


class UploadForm(forms.Form):
	
    fichier = forms.FileField(widget=forms.FileInput(attrs={'id': 'file-0a', 'class': 'file'}), label='Selectionner un fichier...' )
    k = forms.IntegerField()
    n = forms.IntegerField()