import cv2
import numpy as np
import os
import time
import random
from sklearn.cluster import KMeans
from scipy.spatial import distance
from sklearn.preprocessing import normalize


def semantic_clustering(vocab_clusters, num_train_images):
	init_time = time.time()
	numClusters = vocab_clusters

	testImages = os.listdir('/Users/harianbarasu/Desktop/illustra-ligner/extracted-images/')
	testImages = [x for x in testImages if ".jpg" in x]

	sift = cv2.xfeatures2d.SIFT_create()
	BOW = cv2.BOWKMeansTrainer(numClusters)

	for image in testImages:
	  img = cv2.imread('/Users/harianbarasu/Desktop/illustra-ligner/extracted-images/' + image)
	  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	  kp, des = sift.detectAndCompute(gray, None)
	  BOW.add(des)

	dictionary = BOW.cluster()

	# FLANN parameters as taken from OpenCV tutorial
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	sift2 = cv2.xfeatures2d.SIFT_create()
	bowDiction = cv2.BOWImgDescriptorExtractor(sift2, cv2.BFMatcher(cv2.NORM_L2))
	bowDiction.setVocabulary(dictionary)

	def feature_extract(pth):
	    im = cv2.imread(pth, 1)
	    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	    return bowDiction.compute(gray, sift.detect(gray))

	train_desc = []

	for image in testImages:
		train_desc.extend(feature_extract('/Users/harianbarasu/Desktop/illustra-ligner/extracted-images/' + image))
	
	distance_matrix = distance.cdist(train_desc, train_desc, 'euclidean')
	np.savetxt("distance" + str(vocab_clusters) + ".txt", distance_matrix)

	kmeans = KMeans(n_clusters=8).fit(train_desc)

	labels = []
	labels.append(kmeans.labels_)

	sse = []
	sse.append(kmeans.inertia_)

	time_array = []
	time_array.append(time.time() - init_time)

	np.savetxt("labels" + str(vocab_clusters) + ".txt", labels)
	np.savetxt("sse" + str(vocab_clusters) + ".txt", sse)
	np.savetxt("time" + str(vocab_clusters) + ".txt", time_array)


semantic_clustering(5, 50)
print "DONE!"
semantic_clustering(10, 50)
print "DONE!"
semantic_clustering(20, 50)
print "DONE!"
semantic_clustering(50, 50)
print "DONE!"
semantic_clustering(100, 50)
print "DONE!"
semantic_clustering(200, 50)
print "DONE!"
semantic_clustering(500, 50)
print "DONE!"
semantic_clustering(1000, 50)
print "DONE!"
