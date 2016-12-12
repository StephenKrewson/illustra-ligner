#!/usr/bin/python3

import csv
import json
import numpy as np
import os

from collections import OrderedDict
from scipy.spatial import distance

# Get the JSON dict of 2-D embeddings
with open('ID-to-embedding.json', 'r') as fp:
	data = json.load(fp)
	
	# Convert key IDs to ints; keep them in order
	matrix = OrderedDict({int(k):v for k,v in data.items()})
	
	# let's also make a csv thing for using MDS in matlab
	with open('ID-to-embedding.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in matrix.items():
			writer.writerow([value[0],value[1]])
	
	# make a numpy distance matrix
	x = np.array([v[0] for v in matrix.values()]).astype('float')
	y = np.array([v[1] for v in matrix.values()]).astype('float')
	coords = np.column_stack((x,y))
	distances = distance.cdist(coords,coords,'euclidean')
	
	# now munge this into Michael's force-directed format
	json_dict = {'image_dir': os.path.abspath('../../img/extracted')}
	images = os.listdir(json_dict['image_dir'])
	
	nodes = []
	for image in images:
		nodes.append({'id': image})
	json_dict['nodes'] = nodes
	
	links = []
	for i, i1 in enumerate(images):
		print(i,i1)
		for j, i2 in enumerate(images):
			if i == j:
				break
			links.append({'source': i1, 'target': i2, 'distance': distances[i-1,j-1]})
	
	json_dict['links'] = links
	json.dump(json_dict, open('ID-to-distances.json', 'w'))