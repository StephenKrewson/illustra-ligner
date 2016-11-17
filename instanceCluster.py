# Inspiration from
# http://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# http://study.marearts.com/2014/11/opencv-emdearth-mover-distance-example.html

# Ideas 1. have a "set book", and compare images to this set (nearest-nieghbor)
# 1b. Find a better way to represent the results
# 2. Turn the histogram into a channel
import io
import os
import glob
import numpy as np
import cv2
from emd import emd
import argparse

THRESHOLD = .90 # TBD later

def make2DHist(img):
    i = cv2.imread(img)
    cv2.cvtColor(i, cv2.COLOR_BGR2HSV)

    channels = [0,1]
    histSize = [180, 256]
    ranges = [0,180, 0, 256]

    hist = cv2.calcHist([i],channels,None,histSize, ranges)

    # normalizing
    hist = cv2.normalize(hist,0, 1, cv2.NORM_MINMAX).flatten()

    return hist


# imgA and imgB are paths to files
def compareTwoHist(img1, img2, method, opt_args=None):

     imgA = cv2.imread(img1)
     imgB = cv2.imread(img2)

     # Converting from BGR to HSV for color comparison
     cv2.cvtColor(imgA, cv2.COLOR_BGR2HSV)
     cv2.cvtColor(imgB, cv2.COLOR_BGR2HSV)

     # Creating a 2D Histogram
     # hue and saturation
     channels = [0,1]
     histSize = [180, 256]
     ranges = [0,180, 0, 256]

     histA = cv2.calcHist([imgA],channels,None,histSize, ranges)
     histB = cv2.calcHist([imgB],channels,None,histSize, ranges)

     # normalizing
     histA = cv2.normalize(histA,0, 1, cv2.NORM_MINMAX).flatten()
     histB = cv2.normalize(histB,0, 1, cv2.NORM_MINMAX).flatten()

     # compare similarity using earth mover distance or opencv compareHist methods
     # pip install -e git+https://github.com/garydoranjr/pyemd.git#egg=pyemd
     delta = method([histA], [histB] ,opt_args)
     return img1 + ' ' + img2 + ' similarity: ' + str(delta)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required = True,
	   help = "Path to the directory of images")
    args = parser.parse_args()

    image_paths = []

    for f in glob.glob(args.images + "/*.jpg"):
        image_paths.append(f)

    f = open("pairwise_similarity.txt", 'w')

    # find a prefix to determine which book to use
    prefix = image_paths[0].split('/', 2)
    prefix = prefix[2].split('_',1)[0]

    # make k classes from one book
    histograms = []
    for filepath in image_paths:
        if prefix in filepath:
            histograms.append(make2DHist(filepath))

    for i in range(len(image_paths)):
        for j in range(i,len(histograms)):
            # compare histogram to the current image histograms
            if compareTwoHist(image_paths[i], histograms[j], emd) > THRESHOLD:
                print image_paths[i] + 'class ' + str(j)
                exit(0)

            # else make new class
         # f.write(compareTwoHist(image_paths[i],image_paths[j],cv2.compareHist, cv2.HISTCMP_CORREL )+ "\n")
