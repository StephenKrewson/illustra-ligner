import json
import os
from random import random

json_dict = {'image_dir': 'airplanes'}
images = os.listdir(json_dict['image_dir'])[:50]
nodes = []
for image in images:
    nodes.append({'id': image})
json_dict['nodes'] = nodes


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
