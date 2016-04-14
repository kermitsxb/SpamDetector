# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from normalization import Normalizer
import random
import math
import sys

if __name__ == "__main__":
    print "Hello World"

class KMeanClusterer(object):
    
    def getClusterNumber(self):
        """ Retourne le nombre de clusters """
        return self.k
    
    def getCluster(self, index):
        """ Retourne le cluster d'index <index>"""
        if index >= 0 and index < self.k:
            return self.clusters[index]
        else:
            return Cluster()
    
    def assignement(self, step):
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
                    
                
            
            the_cluster.addObservation(tuple(obs))
                 
        self.cleanEmptyClusters()
         
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
        """Calcul le centroide selon les observations actuelles du cluster"""
        observations = cluster.getObservations()
        nbElem = len(observations)
                
        c = self.columns
        cols = [0 for i in range(len(c))]

        # Iterate on cluster observations
        for j in range(nbElem):
            tup = observations[j]

            for k in range(len(cols)):
                cols[k] = cols[k] + float(tup[c[k]])

        # New center
        newBarycentreArray = []
        index = 0
        
        for i in range(self.row_length):
            if i in c:
                #if nbElem > 0:
                newBarycentreArray.append(cols[index] / nbElem)
                #else:
                #    newBarycentreArray.append(0)
                index += 1
            else:
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
                
        return found
    
    def printClusters(self):
        """Affiche les custers et le nb d'elem qu'ils contiennent"""
        for i in range(len(self.clusters)):
            observations = self.clusters[i].getObservations()
            
            print("***** Cluster %d -- %d elements *****" % (i + 1, len(observations)))            
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
            
    def __init__(self, k, columns, datafile):
        """Constructeur pour la classe KMeanClusterer"""
        super(KMeanClusterer, self).__init__()
        
        # Number of clusters wanted
        self.k = k
        
        # columns to work with
        self.columns = columns
        
        # Get CSV data
        norm = Normalizer(datafile)
        self.data = norm.normalize()
        self.row_length = norm.getRowLength()
        self.clusters = []
        
        norm.stats()

        # Find random centroids
        sample = random.sample(range(1, len(self.data)), self.k)
        
        # Create clusters and set random centroid
        for i in range(k):
            cluster = Cluster()
            cluster.setCentroid(self.data[sample[i]])
            self.clusters.append(cluster)
                    
        
        
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
    