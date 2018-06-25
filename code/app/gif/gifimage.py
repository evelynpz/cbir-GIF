"""
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Functions to manage gif files.
"""

# Import the necessary packages
import numpy as np
import cv2

class gifImage:
    def __init__(self, path):
        # Store the path of the image
        self.path = path

    # Return the frames of an gif image
    def getFrames(self):
        # Open the image as a video
        image = cv2.VideoCapture(self.path)
        frames = []

        # Save all the images in the frame list
        while(image.isOpened()):
            ret, frame = image.read()
            if not frame is None:
                frames.append(frame)
            else:
                image.release()

        # Return all the frames
        return frames    

    # Return the average image from a list of frames
    def getAverageImage(self, frames):
        # Travels through all the frames and gets only the average
        avg = np.array(frames[0], dtype=np.float)
        for frame in frames[1:]:
            avg += np.array(frame, dtype=np.float)

        # Round values in the array and cast it as a 8-bit integer
        N = len(frames)
        avg = np.array(np.round(avg/N), dtype=np.uint8)
        return avg
    
    # Show a Gif image
    def showGifImage(self, frames, windowName):
        for frame in frames:
            cv2.imshow(windowName, frame)
            cv2.waitKey(100)
    