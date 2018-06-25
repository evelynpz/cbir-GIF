"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Gradient descriptor using the histogram of oriented gradients (HOG) method.
Ref: https://gurus.pyimagesearch.com/lesson-sample-histogram-of-oriented-gradients-and-car-logo-recognition/
"""

# Import the necesary packages
from skimage import exposure
from skimage import feature
import numpy as np
import cv2

class GradientDescriptor:
    def __init__(self, orientations, pixelsPerCell, cellsPerBlock):
        # Store the values
        self.orientations = orientations
        self.pixelsPerCell = pixelsPerCell
        self.cellsPerBlock = cellsPerBlock
        
    def describe(self, image, transformSqrt=True, visualise=True):
        # Compute the grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Compute the histogram of oriented gradients
        # of the image
        (H, hogImage) = feature.hog(image, this.orientations, this.pixelsPerCell, this.cellsPerBlock, transformSqrt, visualise)