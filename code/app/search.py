"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Search process (full-fledged Content-Based Image Retrieval System)
Usage: python search.py --index index.cpickle --query static/dataset/tumblr_lcpk2tOLoi1qcabl0o1_400.gif --result-path static/dataset
Ref: https://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/
"""

# Import the necessary packages
from descriptors.colordescriptor import ColorDescriptor
from descriptors.texturedescriptor import TextureDescriptor
from descriptors.shapedescriptor import ShapeDescriptor
from similarity.searcher import Searcher
from gif.gifimage import gifImage
from lshash import LSHash
import argparse
import cPickle
import cv2
import datetime

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
               help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
               help = "Path to the query image")
ap.add_argument("-r", "--result-path", required = True,
               help = "Path to the result path")
args = vars(ap.parse_args())

# Start the timer to track how long the searching take
startTime = datetime.datetime.now()

print "[INFO] searching..."

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

# Load the query image
queryI = gifImage(args["query"])
framesQ = queryI.getFrames()
query = queryI.getAverageImage(framesQ)
                     
# Describe the query image
features = []
# Color features:
features.extend(cd.describe(query))
# Texture features:
features.extend(td.describe(query))
# Shape features:
features.extend(sd.describe(query))

# Load the lsh and perform the search
lsh = cPickle.loads(open(args["index"]).read())
results = lsh.query(features, 5, "true_euclidean")

# Print the elapsed time
print "finished!, elapsed time: %d miliseconds" % ((datetime.datetime.now() - startTime).total_seconds() * 1000.0)

# Display the query
queryI.showGifImage(framesQ, "Query")

# Loop over the results
for (resultDescription, score) in results:
    feature, resultID = resultDescription
    # Load the result image and display it
    result = gifImage(args["result_path"] + "/" + resultID)
    result.showGifImage(result.getFrames(), "Result")
    cv2.waitKey(0)