import json
import os
from random import random
import numpy as np

json_dict = {'image_dir': 'thumbnails'}
images = open('imageset.csv').read().split()

nodes = []
for image in images:
    nodes.append({'id': image})
json_dict['nodes'] = nodes

links = []
with open('distance1000.csv') as infile:
    for i, line in enumerate(infile):
        for j, dist_str in enumerate(line.strip().split()):
            if i == j:
                break
            source = images[i]
            target = images[j]
            distance = int(float(dist_str) * 100)
            print(distance)
            links.append({'source': source,
                          'target': target,
                          'distance': distance})

json_dict['links'] = links

json.dump(json_dict, open('sample.json', 'w'))
