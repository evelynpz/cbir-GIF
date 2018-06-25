"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Texture descriptor using the local binary patterns (LBP) method.
Ref: https://www.pyimagesearch.com/2015/12/07/local-binary-patterns-with-python-opencv/
"""

# Import the necesary packages
from skimage import feature
import numpy as np
import cv2

class TextureDescriptor:
    def __init__(self, numPoints, radius):
        # Store the number of points and radius
        self.numPoints = numPoints
        self.radius = radius
        
    def describe(self, image, eps=1e-7):
        # Compute the grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Compute the local binary pattern representation
        # of the image, and then use this to build the 
        # histogram of patterns
        lbp = feature.local_binary_pattern(image, self.numPoints,
                self.radius, method="uniform")
        
        (hist, _) = np.histogram(lbp.ravel(),
                        bins = np.arange(0, self.numPoints + 3),
                        range = (0, self.numPoints + 2))
        
        # Normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)
        
        #Return the histogram of local binary patterns
        return hist