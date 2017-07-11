Rebuilding illustra-ligner
==========================

`illustra-ligner` ingests historical book illustrations that share some similarity (author, printer/publisher, time period, genre, engraving workshop). It then performs instance and semantic clustering on extracted and cleaned up versions of those images.

Currently, the clustering is based on pairwise distances calculated using TensorFlow's pretrained image classification models. See:

https://github.com/tensorflow/models/tree/master/slim




Motivation
----------
The code that I wrote for this project was horribly confusing. Not only was I switching between Python and Matlab, but each of the various scripts lacked one clear purpose. As far as the data images themselves, the naming and folder conventions were unclear. Clarifying how the data should be stored was the first step.


Data Preprocessing
------------------
Extracted images are grouped in a folder whose name is that of the project in upper-case, for instance `PARLEY`. This folder contains three other items:

* A JSON file of nearest-neighbor mappings
* 
 

