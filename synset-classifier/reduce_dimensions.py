
from sklearn.decomposition import NMF
import numpy, glob, json
import scipy.io
import sys

files = glob.glob("./similarity-vectors/*.npy")
vectors = []

# loop over the numpy vectors
for c, i in enumerate(files):
  print("parsing numpy array", c, i)

  # load the vector into memory  
  v = numpy.load(i)

  # convert the vector to an array of floats
  vector = [j for j in v]
  vectors.append(vector)

# build up the master matrix on which we'll perform dimension reduction
X = numpy.array(vectors)

# save to matlab array and quit early
scipy.io.savemat('inception.mat',{'matrix': X})
sys.exit()

# # build the nmf model (non-negative matrix factorization)
# model = NMF(n_components=2, random_state=1)
# model.fit(X)

# # get a matrix with one member for each vector we added to X
# matrix = model.fit_transform(X)
# centered_matrix = matrix / numpy.sum(matrix, axis=1, keepdims=True)  

# # store the reduced dimensionality of each observation
# reduced_dimensionality = {}
# for c, i in enumerate(matrix):
  # reduced_dimensionality[c] = [j for j in i]

# with open("./mappings/ID-to-embedding.json", "w") as out:
  # json.dump(reduced_dimensionality, out)

# # matrix contains one member for each observation
# print(len(matrix))

# # model.components_ contains one member for each topic
# print(model.components_)
