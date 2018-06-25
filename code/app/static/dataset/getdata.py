"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Downloads the data from the file it is given.
Usage: python getdata.py --datafile tgif.tsv --number 2000
"""

# Import the necessary packages
import argparse
import urllib

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--datafile", required = True,
               help = "Path to the file that contains the url of the images to be indexed")
ap.add_argument("-i", "--number", required = True,
               help = "Number of images desired to be substracted from the file")
args = vars(ap.parse_args())

# Number of images to be substracted
max = int(args["number"])
n = 0

# Open the file with the database information
with open(args["datafile"]) as reader:
    
    # Read each line of the file
    for line in reader:
        
        # Verify the number of already downloaded images.
        if n == max:
            break
        else: 
            n += 1
    
        # Extract the image url from the file
        sentence = line.strip().split('\t')
        imageUrl = sentence[0]
        
        # Extract the image ID (i.e. unique filename) from the image
        # url and load the image itself
        imageID = imageUrl[imageUrl.rfind("/") + 1:]
        
        # Download and save the image
        print "[INFO] %d . downloading %s" % (n, imageUrl)
        img = urllib.urlretrieve(imageUrl, imageID)
        
# Show that the download is finished
print "[INFO] finished!"