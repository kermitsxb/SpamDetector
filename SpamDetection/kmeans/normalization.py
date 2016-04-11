import csv
import sys

class Normalizer():

    def show_matrix_dataset(self, iris_data_matrix):
        print("Show matrix dataset")
        for row in iris_data_matrix:
            print(row)
    
    def load_data(self, dataFile):
        
        data_matrix = []
         
        data = open(dataFile,'r')
        reader = csv.reader(data)
        firstLine = True
        rowLength=0
        for row in reader:
            if firstLine:#remove column names
                firstLine = False
                rowLength = len(row)
            elif (len(row) == rowLength):#otherwise remove void lines
                data_matrix.append(row)
        return data_matrix
    
    def find_min_max(self, cols):
        nb_col = len(cols)
        mins = [sys.maxint for i in range(nb_col)]
        maxs = [0 for i in range(nb_col)]
        
        for i in range (len(self.data_cache)):
            line = self.data_cache[i]
            for j in range(nb_col):
                index_col = cols[i]
                
                if line[index_col] > maxs[j]:
                    maxs[j] = line[index_col]
                    
                if line[index_col] < mins[j]:
                    mins[j] = line[index_col]
                    
    def normalize(self, cols):
        bornes = self.find_min_max(cols)
        
        ret = [[]]
        
        
    def __init__(self):
        self.data_cache = []