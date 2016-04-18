# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from normalization import Normalizer
from operator import itemgetter
import random
import math
import sys
import json

if __name__ == "__main__":
    print "Hello World"

class KMeanClusterer(object):
    
    def getClusterNumber(self):
        """ Retourne le nombre de clusters """
        return self.k
    
    def getClusters(self):
        """Retourne la collection de clusters"""
        return self.clusters
    
    def getCluster(self, index):
        """ Retourne le cluster d'index <index>"""
        if index >= 0 and index < self.k:
            return self.clusters[index]
        else:
            return Cluster()
    
    def assignement(self):
        """ Assigne les points du dataset aux clusters selon la distance par rapport aux centroides"""
        # Empty clusters
        for cluster in self.clusters:
            cluster.resetObservations()
        
        # Foreach "line" in dataset
        for obs in self.data:
            global_dist = sys.maxint
            the_cluster = Cluster()
            
            # Foreach cluster : find closest cluster to current line
            for cluster in self.clusters:
                current_dist = self.computeDistance(obs, cluster.getCentroid())
                if current_dist < global_dist:
                    the_cluster = cluster
                    global_dist = current_dist
                    
                
            
            the_cluster.addObservation(obs)
                 
        self.cleanEmptyClusters()
        
    def update(self):
        #Iterations jusqu'a la convergence de l'algorithme
        currentCentroids = self.currentCentroids()
        newCentroids = self.nextCentroids()
        nbIterations = 0

        while self.compareCentroids(currentCentroids, newCentroids) is True:      
            for i in range(self.k):
                currentCluster = self.getCluster(i)
                currentCluster.setCentroid(newCentroids[i])          

            self.assignement()

            currentCentroids = self.currentCentroids()
            newCentroids = self.nextCentroids()

            nbIterations += 1
            
        print("Iterations : %d" % (nbIterations))
         
    def currentCentroids(self):
        """Retourne un tableau contenant les centroides des clusters"""
        centroids = []
        
        for cluster in self.clusters:
            centroids.append(cluster.getCentroid())
            
        return centroids
            
    def nextCentroids(self):
        """Retourne un tableau contenant les centroides calcules des clusters"""
        centroids = []
        
        for cluster in self.clusters:
            centroids.append(self.computeCentroid(cluster))
            
        return centroids
    
    def computeDistance(self, obs, centroid):
        """Calcul une distance entre un point et le centroid selon les colonnes definies"""
        c = self.columns
        somme = 0
        
        # Foreach used column
        for i in range(len(c)):
            somme += (float(obs[c[i]]) - float(centroid[c[i]])) **2
        return math.sqrt(somme)
    
    def computeCentroid(self, cluster):
        """Calcul le centroide selon les observations actuelles du cluster et en renvoi un tuple"""
        observations = cluster.getObservations()
        nbElem = len(observations)
                
        c = self.columns
        
        #Tableau pour conserver les sommes des colonnes avec lesquelles on travaille
        cols = [0 for i in range(len(c))]

        # Iterate on cluster observations
        for j in range(nbElem):
            tup = observations[j]

            for k in range(len(cols)):
                cols[k] = cols[k] + float(tup[c[k]])

        # New center
        newBarycentreArray = []
        index = 0
        
        # Conversion du nouveau centre calcule en tuple avec le meme nombre de champs
        for i in range(self.row_length):
            if i in c: # Si c'est une colonne sur laquelle on travail
                newBarycentreArray.append(cols[index] / nbElem)
                index += 1
            else: #Sinon on ajoute un zero pour garder le meme nombre d'elements dans le tuple
                newBarycentreArray.append(0)
                 
        newBarycentre = tuple(newBarycentreArray)
                
        # Find closest observation to new center
        global_dist = sys.maxint
        found = []
        
        for obs in observations:    
            current_dist = self.computeDistance(obs, newBarycentre)
            if current_dist < global_dist:
                found = obs
                global_dist = current_dist
                
        return tuple(found)
                 
    
    def printClusters(self):
        """Affiche les custers et le nb d'elem qu'ils contiennent"""
        for i in range(len(self.clusters)):
            observations = self.clusters[i].getObservations()
            
            print("***** Cluster %d -- %d elements *****" % (i + 1, len(observations)))
            
            for obs in observations:
                print obs
                
        print("**********************")
        
    def cleanEmptyClusters(self):
        """Supprime les clusters vides"""
        to_delete = []
        
        for cluster in self.clusters:
            if cluster.getObservationsNumber() == 0:
                to_delete.append(cluster)
                
        for cluster in to_delete:
            self.clusters.remove(cluster)
                
        self.k = len(self.clusters)
        
    def compareCentroids(self, set1, set2):
        """Compare deux sets contenant les centroids des clusters"""
        difference = False
        if len(set1) == len(set2):
            for i in range(len(set1)):
                if set1[i] != set2[i]:
                    difference = True
                    break

        return difference
    
    def setRandomCentroids(self):
        # Find random centroids
        sample = random.sample(range(1, len(self.data)), self.k)
        
        # Create clusters and set random centroid
        for i in range(self.k):
            cluster = Cluster()
            cluster.setCentroid(self.data[sample[i]])
            self.clusters.append(cluster)
        
    def performClustering(self):
        """Realisation de toutes les etapes de clustering"""
                
        #Definition de centroides aleatoires
        self.setRandomCentroids()
        
        #Assignement initial
        self.assignement()
        
        #self.printClusters()
        
        #Algorithme principal
        self.update()  
        
        
        
    def findNPercent(self, cluster):
        percentage = self.n / 100.0
        
        observations = cluster.getObservations()
        itemsToFind = int(percentage * len(observations))
        centroid = cluster.getCentroid()

        distances = []
        
        for i in range(len(observations)):
            line = []
            obs = observations[i]
            distance = self.computeDistance(obs, centroid)
            line.append(i)
            line.append(distance)
            distances.append(line)
        
        distances = sorted(distances, key=itemgetter(1), reverse=True)
        
        extracted = []
        for i in range(itemsToFind):
            index = distances[i][0]
            extracted.append(observations[index])
            
        
        return extracted
    
    def toJSON(self):
        out = []
    
        for i in range(self.getClusterNumber()):
            cluster = self.getCluster(i) 
            
            lines = []
            for obs in cluster.getObservations():
                #Coordonnees
                
                if len(self.columns) == 2:
                    x =obs[self.columns[0]]
                    y = obs[self.columns[1]]
                    z = 0
                    
                elif len(self.columns) == 3:
                    x = obs[self.columns[0]]
                    y = obs[self.columns[1]]
                    z = obs[self.columns[2]]
                    
                else:
                    x = 0
                    y = 0
                    z = 0

                lines.append({
                    'x' : x,
                    'y' : y,
                    'z' : z,
                    'isSpam' : obs[self.row_length - 1]
                })
                    
                    
            dict_cluster = {'id' : i+1, 'points' : lines}
            
            out.append(dict_cluster)
            
        print(json.dumps(out))
        
            
    def __init__(self, k, n, columns, datafile):
        """Constructeur pour la classe KMeanClusterer"""
        super(KMeanClusterer, self).__init__()
        
        # Number of clusters wanted
        self.k = k
        self.n = n
        
        # columns to work with
        self.columns = sorted(columns)
        
        # Get CSV data
        norm = Normalizer(datafile)
        self.data = norm.normalize()
        self.row_length = norm.getRowLength()
        self.clusters = []
                            
        
class Cluster(object):
    
    def setCentroid(self, centroid):
        """Defini le centroid <centroid> du cluster"""
        self.centroid = tuple(centroid)
    
    def getCentroid(self):
        """Retourne le centroid courant du cluster"""
        return self.centroid
        
    def getObservations(self):
        """Retourne les observations du cluster"""
        return self.observations
    
    def addObservation(self, obs):
        """Ajoute une observation au cluster"""
        self.observations.append(obs)
        
    def resetObservations(self):
        """Reinitialise les observations du cluster"""
        self.observations = []
        
    def getObservationsNumber(self):
        """Retourne le nombre d'observations dans le cluser"""
        return len(self.observations)
    
    def __init__(self):
        """Constructeur pour la classe Cluster"""
        super(Cluster, self).__init__()
        
        self.resetObservations()
        self.centroid = tuple()
    