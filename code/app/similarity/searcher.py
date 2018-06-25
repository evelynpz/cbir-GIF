"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Define the actual similarity metric between two images.
Ref: https://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/
"""

# Import the necesary packages
import numpy as np
import csv
import math

class Searcher:
    def __init__(self, indexPath):
        # Store the index path
        self.indexPath = indexPath
        
    def search(self, queryFeatures, limit = 5):
        # Initialize the dictionary of results
        results = {}
        
        # Open the index file for reading
        with open(self.indexPath) as f:
            # Initialize the CSV reader
            reader = csv.reader(f)
            
            # Loop over the rows in the index
            for row in reader:
                # Parse out the image ID and features, then compute the
                # chi-squared distance between the features in the index
                # and the query features
                features = [float(x) for x in row[1:]]
                d = self.euclidean(features, queryFeatures)
                
                # With the distance between the two feature vectors,
                # it is possible to update the results dictionary -- the
                # key is the current image ID in the index and the
                # value is the distance that was computed, representing 
                # how 'similar' the image in the index is to the query
                results[row[0]] = d
                
            # Close the reader
            f.close()
            
        # Sort the results, so the smaller distances (i.e the more
        # relevant images are at the front of the list)
        results = sorted([(v, k) for (k, v) in results.items()])
        
        # Return the (limited) results
        return results[:limit]
    
    def chi2_distance(self, histA, histB, eps = 1e-10):
        # Compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) **2) / (a + b + eps)
                         for (a, b) in zip(histA, histB)])
        
        # Return the chi-squared distance
        return d
        
    def euclidean(self, featureA, featureB):
        # Compute the euclidean distance
        d = math.sqrt(np.sum([(a - b)**2
                         for (a, b) in zip(featureA, featureB)]))
        
        # Return the euclidean distance
        return d