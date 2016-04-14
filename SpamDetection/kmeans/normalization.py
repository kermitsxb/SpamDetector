# -*- coding: utf-8 -*-
import csv
import sys

class Normalizer(object):
    
    def getRowLength(self):
        return self.row_length
    
    def show_matrix_dataset(self, iris_data_matrix):
        print("Show matrix dataset")
        for row in iris_data_matrix:
            print(row)
    
    def load_csv(self, dataFile):
        
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
        return self.data_matrix
    
    def find_min_max(self):
        for line in self.data_matrix:
            
            for i in range(self.row_length):
                if float(line[i]) < self.mins[i]:
                    self.mins[i] = float(line[i])
                    
                if float(line[i]) > self.maxs[i]:
                    self.maxs[i] = float(line[i])
    
        print(self.maxs)
        print(self.mins)
        print("-----")
        
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
            ecartype = self.ecartype(column_array, moyenne)
            
            stats_line.append(moyenne)
            stats_line.append(ecartype)
            
            stats.append(stats_line)
            
            print("Colonne %d" % (i))
            print(stats_line)
            print("------")
        
        
        
        return stats
    
    def moyenne(self, array):
        return sum(array, 0.0) / len(array)
    
    def variance(self, array, m):
        return self.moyenne([(x - m)**2 for x in array])
        
    def ecartype(self, array, m):
        return self.variance(array, m) **0.5
    
    def column(self, matrix, i):
        return [row[i] for row in matrix]
    
    def normalize(self):
        normalized = []
        self.find_min_max()
        
        for line in self.data_matrix:
            new_line = []
            for i in range(self.row_length):
                val = float(line[i])
                new_line.append( (val - self.mins[i]) / (self.maxs[i] - self.mins[i]) )
                
            normalized.append(new_line)
        
        self.normalized = normalized
        return self.normalized
        
    def __init__(self, datafile):
        super(Normalizer, self).__init__()
        
        self.data_matrix = []
        self.normalized = []
        self.row_length = 0
        self.line_count = 0
        
        self.load_csv(datafile)
        
        self.mins = [sys.maxint for i in range(self.row_length)]
        self.maxs = [0 for i in range(self.row_length)]
