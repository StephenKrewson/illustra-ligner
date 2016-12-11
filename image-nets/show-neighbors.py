import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import random
import re

def convert_name(fpath):
	img = re.sub(r'.npy','',fpath)
	img = re.sub(r'extracted-sims','extracted-images',img)
	return img

with open('nearest_neighbors.json','r') as fp1, open('data_mapping.json','r') as fp2:
	
	# Load the JSON that maps filepaths to numbers and the nearest-neighbor list
	data = json.load(fp1)
	mapping = json.load(fp2)
	
	# Pick a random image and display its 8 closest neighbors
	k = random.choice(list(data.keys()))

	fig = plt.figure(1, (9., 9.))
	grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(3, 3),  # creates 2x2 grid of axes
                 axes_pad=0.5,  # pad between axes in inch.
				 share_all=True	# force axes to be equal
                 )
	
	for i,nb in enumerate(data[k][:-1]):
	
		# We need to convert from the NP array filename to the plain old image
		path = mapping[str(nb)]
		img = re.sub(r'.npy','',path)
		img = re.sub(r'extracted-sims','extracted-images',img)
		
		# Read in the image
		image = mpimg.imread(img)
		ax = grid[i]
		ax.imshow(image,cmap="Greys_r")
		
		# The title is the year of publication
		year = re.search(r'[0-9]{4,4}',path).group()		
		ax.set_title(year)
		
		# should we also get the similarity score?


plt.show()