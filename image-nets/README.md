# Semantic Clustering with TensorFlow

Our objective is to use a large-scale CNN based on the ImageNet dataset in order to locate the k most similar images for a given image. We use the fact that the penultimate layer of TensorFlow's imagenet module returns a 2048x1 vector of probabilities. The i-th element in this vector gives the confidence [0,1] that the input image matches the i-th of 2048 core ImageNet nodes. These nodes are called synsets and are based on the WordNet database and express the hierarchical structure of a particular lexical concept (e.g. the "hyperonymy" of furniture->bed->bunkbed).

1. `./run-classifier.sh <images_folder>` runs the TensorFlow classifier on each image in the specified folder. The target directory for the numpy arrays of synset probabilities is hard-coded into the `classify_image_mk`. You must have TensorFlow installed as well as Numpy. This step will also generate a JSON mapping of file IDs to their closet lexical match (that is, their most likely synset). One task of validation will be to assess whether these synsets are useful for historical illustration data. 

2. 


# Acknowledgements

Thanks to Douglas Duhaime and Peter Leonard of the Yale Digital Humanities Lab for insipring this approach and sharing their implementation. `classify_image_mk.py` is a fork of (this project)[https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/image/imagenet/classify_image.py]. It follows the ideas in:

http://stackoverflow.com/questions/34809795/tensorflow-return-similar-images

I ran the classify_image_mk.py script on all 28,000 images by using:

find <imagedirectory> -name '*.jpg' | while read file; do python classify_image_mk.py --image_file $file; done