# Inspiration from
# http://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# http://study.marearts.com/2014/11/opencv-emdearth-mover-distance-example.html
import io
import os
import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
from emd import emd
from correctGroups import groupDict

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
def compareTwoHist(img, histB, method, opt_args=None):

     histA = make2DHist(img)

     # compute signal for the two histograms
     numrows = histA.shape[0]

     # compare similarity using earth mover distance or opencv compareHist methods
     # pip install "git+https://github.com/wmayner/pyemd@develop#egg=pyemd"
     delta = method(histA, histB, opt_args)

     return delta

def confusionMatrix(predictions, correct):
    m = len(predictions)
    confusion = np.zeros((m,m))
    g = 0
    total = 0
    for group in predictions:
        for image in group:
            if correct[image] != -1: # no class assignment
                confusion[correct[image], g] += 1
                total += 1
        g += 1
    print total
    print np.trace(confusion) / total
    print confusion

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required = True,
	   help = "Path to the directory of images")
    args = parser.parse_args()

    image_paths = []

    for f in glob.glob(args.images + "/*.jpg"):
        image_paths.append(f)

    f = open("groups.txt", 'w')

    # find a prefix to determine which book to use
    prefix = image_paths[0].split('/', 2)
    prefix = prefix[2].split('_',1)[0]

    # make k classes from one book
    histograms = []
    grouped_images = [[]]
    for filepath in image_paths:
        if prefix in filepath:
            histograms.append(make2DHist(filepath))
            grouped_images.append([filepath])

    for i in range(len(image_paths)):
        temp = [] # storage for comparison
        for j in range(len(histograms)):
            # compare histogram to the current image histograms
             temp.append(compareTwoHist(image_paths[i], histograms[j], cv2.compareHist, cv2.HISTCMP_HELLINGER))
        g = np.argmin(temp)
        grouped_images[g].append(image_paths[i])
            # else make new class (not yet implemented)

    # confusion matrices
    confusionMatrix(grouped_images, groupDict)

    # write results to file
    i = 0
    for group in grouped_images:
        i += 1
        f.write('Group ' + str(i) + '\n')
        for image in group:
            f.write(image + "\n")
        f.write("\n")
