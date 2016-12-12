#!/usr/bin/python3

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
	print(json_dict)
	json.dump(json_dict, open('ID-to-distances.json', 'w'))

'''
def sim(i1, i2):
    if i1 == i2:
        return 0
    elif i1[-6] == i2[-6]:
        return random()
    else:
        return 100

links = []
for i, i1 in enumerate(images):
    for j, i2 in enumerate(images):
        if i == j:
            break
        links.append({'source': i1, 'target': i2, 'distance': sim(i1, i2)})

json_dict['links'] = links
json.dump(json_dict, open('sample.json', 'w'))
'''