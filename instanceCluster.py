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

# input_image, flag (flag determines type of conversion)
cv2.cvtColor(imgA, cv2.COLOR_BGR2HSV)
cv2.cvtColor(imgB, cv2.COLOR_BGR2HSV)

hbins, sbins = 30, 32
channels = [0,1]
histSize = [hbins, sbins]
hranges = [0,180]
sranges = [0, 255]
ranges = np.array([hranges, sranges]).flatten()
#print ranges


# cv2.cvtColor(imgA, patch_HSV, CV_)
#cv2.calcHist(imgA, HistA, None, histSize,ranges)
# hist,bins = np.histogram(imgA.ravel(),256,[0,256])
# images, channels, mask, histSize, ranges,
histA = cv2.calcHist([imgA],channels,None,[180,256], [0,180, 0, 256])
histB = cv2.calcHist([imgB],channels,None,[180,256], [0,180, 0, 256])
# histB = cv2.calcHist([imgB],[0,1,2],None,[8,8,8],[0,256,0,256,0,256])
# histB = cv2.calcHist([imgB],[0],None,[256],[0,256])

# hist = cv2.normalize(hist, hist).flatten()
# plt.plot(histA)
# plt.show()
# plt.plot(histB)
# plt.show()
histA = cv2.normalize(histA,0, 1, cv2.NORM_MINMAX).flatten()
histB = cv2.normalize(histB,0, 1, cv2.NORM_MINMAX).flatten()
#histB = cv2.normalize(histB,histB,0,1,cv2.NORM_MINMAX)

# calculate signal
numrows = hbins * sbins


sig1 = img = np.zeros((numrows, numrows, 3), np.uint8)
sig2 = img = np.zeros((numrows, numrows, 3), np.uint8)
#sig2 = np.zeros((numRows, 3, cv.CV_32FC1)
#
# print histA
# for h in range(hbins):
#      for s in range(sbins):
#         bin_val = histA[h, s]
#         print bin_val
#         sig1[ h*sbins+s, 0] = bin_val
#         sig1[ h*sbins+s, 1] = h
#         sig1[h*sbins+s, 2] = s
#
#         bin_val = histB[h, s]
#         sig2[ h*sbins+s, 0] = bin_val
#         sig2[ h*sbins+s, 1] = h
#         sig2[h*sbins+s, 2] = s


# compare similarity using earth mover distance
# pip install -e git+https://github.com/garydoranjr/pyemd.git#egg=pyemd
print histA.shape
print imgA.shape
e = emd([histA], [histB])
e = e * 100
print 'similarity:'
print e
