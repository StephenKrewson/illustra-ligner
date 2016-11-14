# Adapted from
# http://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# http://study.marearts.com/2014/11/opencv-emdearth-mover-distance-example.html
import io
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy.spatial import distance as dist
from emd import emd

imgA = cv2.imread("./image1.jpg")
imgB = cv2.imread("./image2.jpg")

# Converting from BGR to HSV for color comparison
cv2.cvtColor(imgA, cv2.COLOR_BGR2HSV)
cv2.cvtColor(imgB, cv2.COLOR_BGR2HSV)

# Creating a 2D Histogram
channels = [0,1]
histSize = [180, 256]
ranges = [0,180, 0, 256]

histA = cv2.calcHist([imgA],channels,None,histSize, ranges)
histB = cv2.calcHist([imgB],channels,None,histSize, ranges)

# normalizing
histA = cv2.normalize(histA,0, 1, cv2.NORM_MINMAX).flatten()
histB = cv2.normalize(histB,0, 1, cv2.NORM_MINMAX).flatten()

# compare similarity using earth mover distance
# pip install -e git+https://github.com/garydoranjr/pyemd.git#egg=pyemd
e = emd([histA], [histB])
e = e * 100
print 'similarity:'
print e
