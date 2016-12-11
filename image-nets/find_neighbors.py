from annoy import AnnoyIndex
import random, glob, numpy, json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# path to the numpy arrays
files = glob.glob("../extracted-sims/*.npy")

# number of dimensions in each vector
dims = 2048

# the annoy index
t = AnnoyIndex(dims)

# data mapping maps index position to vector/image name
data_mapping = {}

# nearest neighbors stores a mapping from vector/image index
# to an array of the nearest neighbors (each member of that
# array is an index value of the image within the glob list)
nearest_neighbors = {}

# loop over the numpy vectors
for c, i in enumerate(files):
  data_mapping[c] = i

  # load the vector into memory  
  v = numpy.load(i)

  # convert the vector to an array of floats
  vector = [j for j in v]

  # add the vector to the index
  t.add_item(c, vector)

# store the mapping from index position to image/vector path
with open("data_mapping.json", "w") as out:
  json.dump(data_mapping, out)

# build an index with 10 trees and save the index
t.build(10)
t.save('telescope.ann')

# load the index
u = AnnoyIndex(dims)
u.load('telescope.ann')

# load the data mapping
with open("data_mapping.json") as f:
  data_mapping = json.load(f)

# find the 10 nearest neighbors for each observation
for i in data_mapping.keys():
  print("finding neighbors for", i)
  neighbors = u.get_nns_by_item(int(i), 10)
  nearest_neighbors[i] = neighbors

# store the mapping from each image index value
# to its 10 nearest neighbors
with open("nearest_neighbors.json", "w") as nn_out:
  json.dump(nearest_neighbors, nn_out)
