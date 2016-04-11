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

class KMeanClusterer():
    
    def getClusterNumber(self):
        return self.k
    
    def getCluster(self, index):
        if index >= 0 and index < self.k:
            return self.clusters[index]
        else:
            return Cluster()
    
    def assignement(self):
        current_line = 0
        """
        for obs in self.data:
            global_dist = sys.maxint
            closer = 0
            iterator = 0
            
            for cluster in self.clusters:
                current_dist = self.computeDistance(obs, cluster.getCentroid())
                if current_dist < global_dist:
                    #closer = iterator
                    global_dist = current_dist
                    
                iterator += 1
                
            
            self.clusters[closer].addObservation(tuple(obs))
            current_line += 1
            
        print("Nb itération %d" % (current_line))
        """
        
        print(len(self.data))
        for l in self.data:
            self.clusters[0].addObservation(l)
        
        a = 0
        for i in range(self.k):
            c = self.clusters[i]
            o = c.getObservations()
            a+=len(o)
        print("Total %d" % (a))
            
    
    def computeDistance(self, obs, centroid):
        somme = 0
        for i in range(4):
            somme += (float(obs[i]) - float(centroid[i])) **2
        return math.sqrt(somme)
    
    def __init__(self, k, datafile):
        #super(KMeanClusterer, self, k ,datafile).__init__()
        
        self.k = k
        
        # Get CSV data
        norm = Normalizer()
        self.data = norm.load_csv(datafile)
        self.clusters = []
        
        # Find random centroids
        sample = random.sample(range(1, len(self.data)), self.k)
        
        # Create clusters and set random centroid
        for i in range(k):
            cluster = Cluster()
            cluster.setCentroid(self.data[sample[i]])
            self.clusters.append(cluster)
                    
        
        
class Cluster():
    
    def setCentroid(self, centroid):
        self.centroid = tuple(centroid)
    
    def getCentroid(self):
        return self.centroid
    
    def getObservations(self):
        return self.observations
    
    def addObservation(self, obs):
        self.observations.add(deepcopy(tuple(obs)))
    
    def __init__(self):
        #super(Cluster, self).__init__()
        
        self.observations = set()
        self.centroid = tuple()
