"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Flask application.
Ref: https://www.pyimagesearch.com/2014/12/08/adding-web-interface-image-search-engine-flask/
"""

import os

from flask import Flask, render_template, request, jsonify

from descriptors.colordescriptor import ColorDescriptor
from descriptors.texturedescriptor import TextureDescriptor
from descriptors.shapedescriptor import ShapeDescriptor
from similarity.searcher import Searcher
from gif.gifimage import gifImage
from lshash import LSHash
import cPickle
import cv2
import datetime

# Create flask instance
app = Flask(__name__, static_url_path = '', static_folder = 'static')
# Specify paths
STATICPATH = os.path.dirname(__file__) + '/static/'
INDEX = os.path.join(os.path.dirname(__file__), 'index.cpickle')

# Main route
@app.route('/')
def index():
    return render_template('index.html')

# Search route
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        RESULTS_ARRAY = []
        
        # Get url
        image_url = STATICPATH + request.form.get('img')
        
        try:
            
            # start the timer to track how long the indexing take
            startTime = datetime.datetime.now()
            
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
            
            # Load the query image, average and describe it
            queryI = gifImage(image_url)
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
            lsh = cPickle.loads(open(INDEX).read())
            results = lsh.query(features, 5)

            # Loop over the results, displaying the sore and image name
            for (resultDescription, score) in results:
                feature, resultID = resultDescription
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})
            
            # return success
            return jsonify(results=(RESULTS_ARRAY), time=(datetime.datetime.now() - startTime).total_seconds() * 1000.0)
            
        except:
            
            # Return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500
        

# Run
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)