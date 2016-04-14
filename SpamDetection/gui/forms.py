from django import forms
from django.core.files import File


class UploadForm(forms.Form):
    fichier = forms.FileField()
    k = forms.IntegerField()
    n = forms.IntegerField()
