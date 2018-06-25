"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Shape descriptor using Zernike moments.
Ref: https://www.pyimagesearch.com/2014/04/07/building-pokedex-python-indexing-sprites-using-shape-descriptors-step-3-6/
"""

# Import the necesary packages
import mahotas
import cv2
import numpy as np

class ShapeDescriptor:
    def __init__(self, radius):
        # Store the size of the radius that will be 
        # used when computing moments
        self.radius = radius
        
    def describe(self, image):
        # Compute the grayscale image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Pad the image with extra white pixels to ensure the
        # edges of the image are not up against the borders
        # of the image
        image = cv2.copyMakeBorder(image, 15, 15, 15, 15, 
                    cv2.BORDER_CONSTANT, value = 255)
        
        # Invert the image and threshold it
        thresh = cv2.bitwise_not(image)
        thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
	cv2.THRESH_BINARY_INV, 11, 7)
        # Initialize the outline image, find the outermost
        # contours (the outline) of the image, then draw it
        #outline = np.zeros(image.shape, dtype = "uint8")
        #(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        #                cv2.CHAIN_APPROX_SIMPLE)
        #cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        #cv2.drawContours(outline, [cnts], -1, 255, -1)
        
        #cv2.imshow("a", thresh)
        #cv2.waitKey(0)
        
        # Return the Zernike moments for the image
        return mahotas.features.zernike_moments(thresh, self.radius)