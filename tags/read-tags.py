#!/usr/bin/python3

import json
import os
import sys

if len(sys.argv) !=2:
	exit('Usage: ./read-tags.py <JSON_file>')

with open(sys.argv[1]) as f:
	tags = json.load(f)
	
tagset = set()	
	
for key in tags:
	tagset = tagset.union(tags[key]['tags'])
	
with open('taglist.txt','w') as f:
	f.write('\n'.join(list(tagset)));