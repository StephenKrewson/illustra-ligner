import json
import os
import sys

# Look for JPEG files in the current directory
folder = './'

# turn dict object into JSON
tags = {}

for fn in os.listdir(folder):

	if fn.endswith('.jpg'):
	
		tags[fn] = {
			'wnid': '',
			'year': '',
			'tags': [],
		}
		year = fn.split('_')[0]
		tags[fn]['year'] = year		


print(json.dumps(tags, sort_keys=True))

# NB difference between dumps and dump (printing vs. writing)
with open('tags.json', 'w') as t:
	json.dump(tags, t, sort_keys=True)