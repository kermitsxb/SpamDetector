# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from normalization import Normalizer
import random
import math
import sys
from copy import deepcopy

if __name__ == "__main__":
    print "Hello World"

class KMeanClusterer(object):
    
    def getClusterNumber(self):
        return self.k
    
    def getCluster(self, index):
        if index >= 0 and index < self.k:
            return self.clusters[index]
        else:
            return Cluster()
    
    def assignement(self, step):
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
        centroids = []
        
        for cluster in self.clusters:
            centroids.append(cluster.getCentroid())
            
        return centroids
            
    def nextCentroids(self):
        centroids = []
        
        for cluster in self.clusters:
            centroids.append(self.computeCentroid(cluster))
            
        return centroids
    
    def computeDistance(self, obs, centroid):
        c = self.columns
        somme = 0
        
        # Foreach used column
        for i in range(len(c)):
            somme += (float(obs[c[i]]) - float(centroid[c[i]])) **2
        return math.sqrt(somme)
    
    def computeCentroid(self, cluster):
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
            
        # TP3 Specific
        #newBarycentreArray.append("")
        
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
        for i in range(len(self.clusters)):
            observations = self.clusters[i].getObservations()
            spams = 0
            nospams = 0
            
            print("***** Cluster %d -- %d elements *****" % (i + 1, len(observations)))
            for obs in observations:
                if float(obs[57]) == 1:
                    spams += 1
                else:
                    nospams += 1
                    
            print("\t %d spams, %d non spams" % (spams, nospams))
            
        print("**********************")
        
    def cleanEmptyClusters(self):
        to_delete = []
        
        for cluster in self.clusters:
            if cluster.getObservationsNumber() == 0:
                to_delete.append(cluster)
                
        for cluster in to_delete:
            self.clusters.remove(cluster)
                
        self.k = len(self.clusters)
            
    def __init__(self, k, columns, datafile):
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
        self.centroid = tuple(centroid)
    
    def getCentroid(self):
        return self.centroid
        
    def getObservations(self):
        return self.observations
    
    def addObservation(self, obs):
        self.observations.append(obs)
        
    def resetObservations(self):
        self.observations = []
        
    def getObservationsNumber(self):
        return len(self.observations)
    
    def __init__(self):
        super(Cluster, self).__init__()
        
        self.resetObservations()
        self.centroid = tuple()
    