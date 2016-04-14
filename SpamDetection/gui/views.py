#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
	return render(request, 'gui/index.html')

def upload(request):

	if request.method == 'POST':  # S'il s'agit d'une requête POST

	    form = UploadForm(request.POST)  # Nous reprenons les données


	    if form.is_valid(): # Nous vérifions que les données envoyées sont valides


	        # Ici nous pouvons traiter les données du formulaire

	        fichier = form.cleaned_data['file']

	        k = form.cleaned_data['k']

	        n = form.cleaned_data['n']



	else: # Si ce n'est pas du POST, c'est probablement une requête GET

	    form = UploadForm()  # Nous créons un formulaire vide


	    return render(request, 'gui/form_temp.html', locals())
