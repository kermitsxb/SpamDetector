import unittest

from normalization import Normalizer
from kmeans import KMeanClusterer


class Test(unittest.TestCase):


    def setUp(self):
        self.datafile = "datasets/spambase_2.data"
        self.normalizer = Normalizer(self.datafile)
        
        pass


    def tearDown(self):
        pass

    def getDatasetSize(self, datafile):

        norm = Normalizer()
        iris_data_matrix = norm.load_csv(datafile)
        return len(iris_data_matrix)

    def testKMean(self):
        print("** test KMean **")
        
        # perform initialization
        k = 3
        n = 10
        cols = [3,4,5]
        
        kMeanClusterer = KMeanClusterer(k,n,cols,self.datafile)
        kMeanClusterer.performClustering()
        
        #total number of lines in the dataset
        dataLines = 0

        data_matrix = self.normalizer.get_csv()
        for row in data_matrix:
            if len(row) > 0:
                dataLines += 1

        #check the number of observations from dataset is kept        
        totalObsNb = 0
        for clusterNb in range(kMeanClusterer.getClusterNumber()):
            cluster = kMeanClusterer.getCluster(clusterNb)
            totalObsNb += len(cluster.getObservations())
        
        self.assertTrue(dataLines == totalObsNb, "Number of entries in dataset: "+str(dataLines)
                        +" is different from number of observations in cluster: "+str(totalObsNb))
        
        # check all normalized entries in the dataset are kept
        index = 0
        for entry in self.normalizer.normalize():
            found = False
            for clusterNb in range(kMeanClusterer.getClusterNumber()):
                cluster = kMeanClusterer.getCluster(clusterNb)
                observations = cluster.getObservations()
                for obs in observations:
                    
                    if obs == entry:
                        found = True
                        break
                        
            self.assertTrue(found, "observation "+str(entry)+" not found at index "+str(index))
            index += 1
            
    def testKMeanUpdate(self):
        print("** test KMean update **")
        
        k = 3
        n = 10
        cols = [3,4,5]
        
        datafile="datasets/spambase_2.data"
        kMeanClusterer = KMeanClusterer(k,n,cols,datafile)
        
        kMeanClusterer.assignement()
        kMeanClusterer.update()
        
        # check existence of centroid
        for i in range(kMeanClusterer.getClusterNumber()):
            current_cluster = kMeanClusterer.getCluster(i)
            self.assertTrue(len(current_cluster.getCentroid()) > 0, "void centroid for cluster "+str(i))
        
        # check validity of centroid
        for i in range(kMeanClusterer.getClusterNumber()):
            current_cluster = kMeanClusterer.getCluster(i)
            current_centroid = current_cluster.getCentroid()
            obs = current_cluster.getObservations()
            for j in range(len(current_centroid)):
                tmp = 0
                for i in range(len(obs)):
                    try:
                        tmp += float(obs[i][j])
                    except ValueError:
                        pass # field is not numeric
                try:
                    value = float(current_centroid[j])#for test that data is numeric
                    self.assertTrue(tmp/len(obs) == value, "current centroid: "+str(value)
                                +"; actual centroid value: "+str(tmp/len(obs)))
                except ValueError:
                        pass # field is not numeric

    def testCentroidsComparison(self):
        print("** Test centroids comparison **")
        
        k = KMeanClusterer(3,10, [3,4,5], "datasets/spambase_2.data")
        
        centroid1 = tuple([1,2,3,4,5])
        centroid2 = tuple([1,2,3,4,5])
        centroid3 = tuple([5,4,3,2,6])
        
        centroidsEquals1 = [centroid1, centroid1]
        centroidsEquals2 = [centroid2, centroid2]
        
        centroidsDifferents1 = [centroid1, centroid1]
        centroidsDifferents2 = [centroid1, centroid3]

        self.assertTrue(k.compareCentroids(centroidsEquals1, centroidsEquals2) == False , "Centroids should be equals")
        
        self.assertTrue(k.compareCentroids(centroidsDifferents1, centroidsDifferents2), "Centroids should be different")

    def testCalculations(self):
        print("** Mean test **")
        
        arr = [10,15,20]
        moy = 15
        
        self.assertTrue(self.normalizer.moyenne(arr) == moy, "Mean calculation is uncorrect")

    def testColumnExtraction(self):
        print("** Test column extraction **")
        
        multi = [
            [1,2],
            [3,4],
            [5,6],
            [7,8],
            [9,0]
        ]
        
        single = [1,3,5,7,9]
        
        self.assertTrue(self.normalizer.column(multi, 0) == single, "Extracted column doesn't match")


    def testNormalization(self):
        print("** Test normalization **")
        
        the_normalizer = Normalizer("datasets/test_normalization.csv")
        
        normalized = [
            [0,0,0],
            [1,1,1],
            [0.5, 0.1, 0.9]
        ]
        
        self.assertTrue(the_normalizer.normalize() == normalized, "Normalized data doesn't match")
        
    def testCSVIntegrity(self):
        print("** Test CSV Integrity **")
        
        the_normalizer = Normalizer("datasets/test_normalization.csv")
        
        data = the_normalizer.get_csv()
        
        origin_data = [
            ['0','3','0'],
            ['1','33','100'],
            ['0.5', '6', '90']
        ]
        
        length = 3
        
        self.assertTrue(data == origin_data, "Data and CSV file doesn't match")
        self.assertTrue(length == the_normalizer.getRowLength(), "Line length doesn't match")

if __name__ == "__main__":
    unittest.main()