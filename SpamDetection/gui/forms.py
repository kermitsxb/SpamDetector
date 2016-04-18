from django import forms
from django.core.files import File
from django.core.validators import *


class UploadForm(forms.Form):
	
    fichier = forms.FileField(widget=forms.FileInput(attrs={'id': 'file-0a', 'class': 'file'}), label='Selectionner un fichier...' )
    k = forms.IntegerField(validators=[MinValueValidator(1)])
    n = forms.IntegerField(validators=[MinValueValidator(1)])
