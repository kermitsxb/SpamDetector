# -*- coding: utf-8 -*-
import csv
import sys

class Normalizer(object):
    
    def getRowLength(self):
        """Retourne la longueur d'une ligne du dataset"""
        return self.row_length
    
    def show_matrix_dataset(self, iris_data_matrix):
        """Affiche le dataset"""
        print("Show matrix dataset")
        for row in iris_data_matrix:
            print(row)
    
    def load_csv(self, dataFile):
        """Recupere les donnees du dataset dans une variable locale"""
        data_matrix = []
         
        data = open(dataFile,'r')
        reader = csv.reader(data)
        firstLine = True
        row_length=0
        self.row_length = 0
        
        for row in reader:
            if firstLine:#remove column names
                firstLine = False
                row_length = len(row)
                self.row_length = row_length
                
            if (len(row) == row_length):#otherwise remove void lines
                data_matrix.append(row)
                
            self.line_count += 1
            
            
        self.data_matrix = data_matrix        

    def get_csv(self):
        """Renvoi les donnees du dataset depuis une variable"""
        return self.data_matrix
    
    def find_min_max(self):
        """ Recupere les minimums et maximums pour chaque colonne sur l'espace non normalise"""
        for line in self.data_matrix:
            
            for i in range(self.row_length):
                if float(line[i]) < self.mins[i]:
                    self.mins[i] = float(line[i])
                    
                if float(line[i]) > self.maxs[i]:
                    self.maxs[i] = float(line[i])
        
    def stats(self):
        """Retourne les statistiques pour chaque colonne sous la formes stats[col_index] = [min, max, moyenne, ecart_type]"""
        stats = []        
        # Si on a pas normalise avant
        if len(self.normalized) == 0:
            self.normalize()
                
        #Stats pour chaque colonne
        for i in range(self.row_length):
            stats_line = []
            
            column_array = self.column(self.normalized, i)
            
            stats_line.append(min(column_array))
            stats_line.append(max(column_array))
            
            moyenne = self.moyenne(column_array)
            ecartype = self.ecartype(column_array)
            
            stats_line.append(moyenne)
            stats_line.append(ecartype)
            
            stats.append(stats_line)      
        
        return stats
    
    def moyenne(self, array):
        """Retourne la moyenne des valeurs d'un tableau"""
        return sum(array, 0.0) / len(array)
    
    def variance(self, array):
        """Retourne la variance des valeurs d'un tableau"""
        return self.moyenne([(x - self.moyenne(array))**2 for x in array])
        
    def ecartype(self, array):
        """Retourne l'ecart type des valeurs d'un tableau"""
        return self.variance(array) **0.5
    
    def column(self, matrix, i):
        """Renvoi une colonne d'un tableau multi dimensionnel en tant que tableau 1-D"""
        return [row[i] for row in matrix]
    
    def normalize(self):
        """Normalise les donnees du dataset entre 0 et 1"""
        normalized = []
        self.find_min_max()
        
        for line in self.data_matrix:
            new_line = []
            for i in range(self.row_length):
                val = float(line[i])             
                
                if self.maxs[i] > 0 and self.maxs[i] > self.mins[i]:
                    new_line.append( (val - self.mins[i]) / (self.maxs[i] - self.mins[i]) )
                else:
                    new_line.append( val )
                    
            normalized.append(new_line)
        
        self.normalized = normalized
        
        return self.normalized
        
    def __init__(self, datafile):
        """Constructeur pour la classe Normalizer"""
        super(Normalizer, self).__init__()
        
        self.data_matrix = []
        self.normalized = []
        self.row_length = 0
        self.line_count = 0
        
        self.load_csv(datafile)
        
        self.mins = [sys.maxint for i in range(self.row_length)]
        self.maxs = [0 for i in range(self.row_length)]
