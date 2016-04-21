#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from gui.forms import UploadForm
from gui.models import Document

from kmeans.normalization import Normalizer
from kmeans.kmeans import KMeanClusterer, Cluster
import sys
import csv
import json

kMeanClusterer = None


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
	        #return statistiques(request)	
	        return HttpResponseRedirect(reverse('stats'))
	                

	else: # Si ce n'est pas du POST, c'est probablement une requête GET

	    form = UploadForm()  # Nous créons un formulaire vide

    	return render(request, 'gui/form_temp.html', {'form': form})

#Fonction affichant l'écran 2 où est éxecuté l'algorithme de KMean et 
# sont faites les statistiques
def statistiques(request):
	datafile = settings.MEDIA_ROOT + request.session['cheminFichier']

	norm = Normalizer(datafile)
	data = norm.normalize()
	row_length = norm.getRowLength()

	stats = norm.stats()

	request.session['page'] = 'stats'

	data_name = open("data_names", "r")
	print >>sys.stderr, '[DEBUG] K : ' + str(request.session['k'])
	print >>sys.stderr, '[DEBUG] N : ' + str(request.session['n'])

	html_head = ""
	html_body = ""
	html_stat = ""
	html_foot = ""

	html_head += "<th></th>"

	chkValue = 0;

	for line in data_name:
		html_head += "<th><INPUT id=" + str(line) + " type=\"checkbox\" name=" + str(line) + " onclick='handleCheckbox(this);' value="+str(chkValue)+"> " + str(line) + "</th>"
		chkValue += 1
	
	data_name.close()

	nRow = 1

	for row in data:
		html_body += "<tr>"
		html_body += "<td>" + str(nRow) + "</td>"
		for col in row:
			html_body += "<td>" + str(col) + "</td>"

		html_body += "</tr>"
		nRow += 1

	#html_empty = "<tr class=""blank_row""><td colspan=" + str(row_length) + "></td></tr>"

	#print >>sys.stderr, '[DEBUG] Stats[5][1] : ' + str(stats[5][1])
	html_foot += "<tr><th></th>"
	data_name = open("data_names", "r")
	for line in data_name:
		html_foot += "<th>" + str(line) + "</th>"
	data_name.close()

	html_foot += "</tr>"

	for j in range(0, 4):
		tab = norm.column(stats, j)
		html_foot += "<tr>"

		if j == 0:
			html_foot += "<td>Min</td>"
		elif j == 1:
			html_foot += "<td>Max</td>"
		elif j == 2:
			html_foot += "<td>Moy</td>"
		elif j == 3:
			html_foot += "<td>ET</td>"

		# print >>sys.stderr, '[DEBUG] J : ' + str(j)
		for i in range(0, len(tab)):
			html_foot += "<td>" + str(tab[i]) + "</td>"
			# print >>sys.stderr, '[DEBUG] I : ' + str(i)

		html_foot += "</tr>"

	return render(request, 'gui/stat_temp.html', {'thead': html_head, 'tbody': html_body, 'tstats': html_stat, 'tfoot': html_foot})

#Fonction qui appelle la vue générant les graphiques d3js pour l'affichage
# des résultats du KMean algorithm
def graphique(request):
	cols = request.GET['cols']
	colonne = []
	nb = 0
	for col in cols.split(","):
		if int(col) != -1:
			nb+=1
			# print >>sys.stderr, '[DEBUG] append : ' + str(col)
			colonne.append(int(col))
	k = request.session['k']
	n = request.session['n']
	datafile = settings.MEDIA_ROOT + request.session['cheminFichier']
	print >>sys.stderr, '[DEBUG] cols : ' + str(cols)
	print >>sys.stderr, '[DEBUG] k : ' + str(k)
	print >>sys.stderr, '[DEBUG] n : ' + str(n)
	print >>sys.stderr, '[DEBUG] datafile : ' + str(datafile)

	global kMeanClusterer

	kMeanClusterer = KMeanClusterer(k, n, colonne, datafile)
	kMeanClusterer.performClustering()
	#kMeanClusterer.setRandomCentroids()
	#kMeanClusterer.assignement()
	# kMeanClusterer.update()
        
	mon_json = kMeanClusterer.toJSON()

	#print >>sys.stderr, '[DEBUG] json : ' + str(mon_json)

	return render(request, 'gui/graph_temp.html', {'data': mon_json, 'nb_arg': nb, 'k': k, 'n': n, 'step': 0})

# Fonction qui passe à l'étape suivante dans le kmean via ajax
@csrf_exempt
def updateKMean(request):
	step_nb = int(request.POST.get("step").encode('ascii','ignore')) + 1
	k = int(request.POST.get("k").encode('ascii','ignore')) + 1
	n = int(request.POST.get("n").encode('ascii','ignore')) + 1
	nb = -1

	print >>sys.stderr, '[DEBUG] step_nb : ' + str(step_nb)

	global kMeanClusterer

	kMeanClusterer.manualUpdate()
	if kMeanClusterer.isOver():
		print >>sys.stderr, 'L\'algorithme a convergé!'
		return HttpResponse("FIN")
	else:
		mon_json = kMeanClusterer.toJSON()
		return HttpResponse(
	        mon_json,
	        content_type="application/json"
	    )

	
	#print >>sys.stderr, '[DEBUG] json : ' + str(mon_json)
	
	# return render(request, 'gui/graph_temp.html', {'data': mon_json, 'nb_arg': nb, 'k': k, 'n': n, 'step': step_nb})

