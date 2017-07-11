Rebuilding illustra-ligner
==========================

`illustra-ligner` ingests historical book illustrations that share some similarity (author, printer/publisher, time period, genre, engraving workshop). It then performs instance and semantic clustering on extracted and cleaned up versions of those images.

Currently, the clustering is based on pairwise distances calculated using TensorFlow's pretrained image classification models. See:

https://github.com/tensorflow/models/tree/master/slim

https://www.tensorflow.org/tutorials/image_recognition

https://www.tensorflow.org/tutorials/image_retraining

https://github.com/eldor4do/TensorFlow-Examples/blob/master/retraining-example.py


TODO


Tools
-----
* OS: Windows 10 (fast ring insider previews)
* Anaconda environment with Python 3.5; run from Anaconda prompt (`cmd.exe`) since there are endless annoyances with WSL and PowerShell and virtualenv

> `activate tensorflow`

* scikit-learn, scikit-image, numpy (the goal is to only use open-source tools importable through `conda`---no Matlab)


Motivation
----------
The code that I wrote for this project was horribly confusing. Not only was I switching between Python and Matlab, but each of the various scripts lacked one clear purpose. As far as the data images themselves, the naming and folder conventions were unclear. Clarifying how the data should be stored was the first step.


Data Preprocessing
------------------
Extracted images are grouped in a folder whose name is that of the project in upper-case, for instance `PARLEY`. This folder contains three other items:

* A JSON file of nearest-neighbor mappings
* 
 






# Semantic Clustering with TensorFlow

Our objective is to use a large-scale CNN based on the ImageNet dataset in order to locate the k most similar images for a given image. We use the fact that the penultimate layer of TensorFlow's imagenet module returns a 2048x1 vector of probabilities. The i-th element in this vector gives the confidence [0,1] that the input image matches the i-th of 2048 core ImageNet nodes. These nodes are called synsets and are based on the WordNet database and express the hierarchical structure of a particular lexical concept (e.g. the "hyperonymy" of furniture->bed->bunkbed).

1. `./run-classifier.sh <images_folder>` runs the TensorFlow classifier on each image in the specified folder. The target directory for the numpy arrays of synset probabilities is hard-coded into the `classify_image_mk`. You must have TensorFlow installed as well as Numpy. This step will also generate a JSON mapping of file IDs to their closet lexical match (that is, their most likely synset). One task of validation will be to assess whether these synsets are useful for historical illustration data. 

2. 


# Acknowledgements

Thanks to Douglas Duhaime and Peter Leonard of the Yale Digital Humanities Lab for insipring this approach and sharing their implementation. `classify_image_mk.py` is a fork of (this project)[https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/image/imagenet/classify_image.py]. It follows the ideas in:

http://stackoverflow.com/questions/34809795/tensorflow-return-similar-images

I ran the classify_image_mk.py script on all 28,000 images by using:

find <imagedirectory> -name '*.jpg' | while read file; do python classify_image_mk.py --image_file $file; done