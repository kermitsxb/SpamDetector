#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from gui.forms import UploadForm
from gui.models import Document

from kmeans.normalization import Normalizer
import sys


# Vue de base ./
def home(request):
	return render(request, 'gui/index.html')

# Créer la vue pour l'upload des fichiers et la saisie des critères
def upload(request):
	request.session['page'] = 'upload'

	if request.method == 'POST':  # S'il s'agit d'une requête POST

	    form = UploadForm(request.POST, request.FILES)  # Nous reprenons les données

	    if form.is_valid(): # Nous vérifions que les données envoyées sont valides
	    	#Sauvegarde du fichier reçu dans ~/media/documents
	    	newdoc = Document(fichier = request.FILES['fichier'])
	    	newdoc.save()

	        # Ici nous pouvons traiter les données du formulaire
	        #fichier = form.cleaned_data['file']
	        k = form.cleaned_data['k']
	        n = form.cleaned_data['n']

	        print >>sys.stderr, '[DEBUG] page : ' + str(request.session['page'])
	        print >>sys.stderr, '[DEBUG] file : /media/document/' + str(form.cleaned_data['fichier'])
	        print >>sys.stderr, '[DEBUG] K : ' + str(k)
	        print >>sys.stderr, '[DEBUG] N : ' + str(n)
	        print >>sys.stderr, '[DEBUG] MEDIA_ROOT : ' + str(settings.MEDIA_ROOT)


	        # Ajout des données dans la session
	        request.session['cheminFichier'] = '/documents/' + str(form.cleaned_data['fichier'])
	        request.session['k'] = k
	        request.session['n'] = n

	        print >>sys.stderr, settings.MEDIA_ROOT + request.session['cheminFichier']


	        return statistiques(request, k, n)


	else: # Si ce n'est pas du POST, c'est probablement une requête GET

	    form = UploadForm()  # Nous créons un formulaire vide

    	return render(request, 'gui/form_temp.html', {'form': form})

#Fonction affichant l'écran 2 où est éxecuté l'algorithme de KMean et 
# sont faites les statistiques
def statistiques(request, k, n):
	datafile = settings.MEDIA_ROOT + request.session['cheminFichier']

	norm = Normalizer(datafile)
	data = norm.normalize()

	stats = norm.stats

	request.session['page'] = 'stats'

	return render(request, 'gui/stat_temp.html')


#Fonction qui appelle la vue générant les graphiques d3js pour l'affichage
# des résultats du KMean algorithm
def graphique(request):

	return render(request, 'gui/graph_temp.html')