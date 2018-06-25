"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Indexation process which extracts the features and stores them on a persistent storage.
Usage: python index.py --dataset static/dataset --index index.cpickle
Ref: https://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/
"""

# Import the necessary packages
from descriptors.colordescriptor import ColorDescriptor
from descriptors.texturedescriptor import TextureDescriptor
from descriptors.shapedescriptor import ShapeDescriptor
from gif.gifimage import gifImage
from lshash import LSHash
import argparse
import cPickle
import glob
import cv2
import datetime

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
               help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
               help = "Path where the computed index will be stored")
args = vars(ap.parse_args())

# Start the timer to track how long the indexing take
startTime = datetime.datetime.now()

print "[INFO] indexing images ..."

# Initialize the color descriptor, all images will
# be represented using a list of 288 floating point numbers.
# Hue: 8 bins
# Saturation: 12 bins
# Value: 3 bins
cd = ColorDescriptor((8, 12, 3))

# Initialize the texture descriptor, all images will
# be represented using a list of 26 (p + 2) floating point numbers.
# Number of points: 24
# Radius: 8
td = TextureDescriptor(24, 8)

# Initialize the shape descriptor (Zernike Moments with a radius
# of 21 used to characterize the shape of all images)
sd = ShapeDescriptor(21)

# Initialize the index dictionary to store the quantifed 
# images, with the 'key' of the dictionary being the image
# filename and the 'value' the computed features.
sizelsh = 288+26+25 # 288 for color, 26 for texture, 25 for shape.
lsh = LSHash(9, sizelsh, 1, None, "lshash-matrix.npz", True)

# Use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.gif"):
    
    # Extract the image ID (i.e. the unique filename) from the image 
    # path and load the image itself
    imageID = imagePath[imagePath.rfind("/") + 1:]
	
    # Create a gif image class and get the average image
    gif = gifImage(imagePath)
    avg = gif.getAverageImage(gif.getFrames())
    
    # Get the features from the average image
    features = []
    # Color features:
    features.extend(cd.describe(avg))
    # Texture features:
    features.extend(td.describe(avg))
    # Shape features:
    features.extend(sd.describe(avg))
    
    # Update the index
    lsh.index(features, imageID)

# Done indexing the images, now write the index to the disk
f = open(args["index"], "w")
f.write(cPickle.dumps(lsh))
f.close()

# Print the elapsed time
print "[INFO] finished!, elapsed time: %d seconds" % (datetime.datetime.now() - startTime).total_seconds()