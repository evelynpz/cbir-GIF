"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Color descriptor using a 3D histogram in the HSV color space.
Ref: https://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/
"""

# Import the necesary packages
import numpy as np
import cv2

class ColorDescriptor:
    def __init__(self, bins):
        # Store the number of bins for the 3D histogram
        self.bins = bins
        
    def describe(self, image):
        # Convert the image to the HSV color space
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Compute a 3D histogram in the HSV colorspace,
        # then normalized so the images with same content,
        # but either scaled larger or samller will have (roughly)
        # the same histogram
        hist = cv2.calcHist([image], [0, 1, 2],
            None, self.bins, [0, 180, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist)
        
        # Return out the 3D histogram as a flattened array
        return hist.flatten()