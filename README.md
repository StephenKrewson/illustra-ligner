illustra-ligner
===============

Origin
------
`illustra-ligner` is a pipeline for clustering historical book illustrations. We support both exact matches ("instance clustering") and lower-dimensional groupings based on some latent structure in the data ("semantic clustering"). This began as a final project for Guy Wolf's CPSC 545, Introduction to Data Mining at Yale University, Fall 2016.

Team members were Hari Anbarasu, Stephen Krewson, Michael Menz, and Rachel Prince. At the time, the four of us were all teaching assistants for [CS50](cs50.yale.edu).

I (Stephen Krewson) reorganized much of the codebase over summer 2017 in preparation for my master's thesis. Specific updates are discussed below. 


Datasets
--------
* Tom Telescope (TT): 130 images from ECCO (low-resolution microfilm scans)
* Peter Parley (PP): 3000+ images from InternetArchive (many medium-resolution scans from Google Books)

TODO
* For Parley/Goodrich images, migrate to HathiTrust (figuring out where to store them) 


Transfer Learning with TensorFlow and ImageNet
----------------------------------------------
With the

The pipeline is:

* Run the classifier

> `run-classifier.sh`

* Convert numpy arrays to .mat format

> `reduce_dimensions.py`

* Try out Laurens van der Maatens toolbox (everything hardcoded)

> `reduce.m`

* Build distance matrix (either brute-force Euclidean or with Spotify's AnnoyIndex)

* Create good visualizations (I am not spending enough time on this part!!)


https://github.com/spotify/annoy

TODO
----
* Transfer from Inception v2 to v4 (using TF Slim)
* It really needs to be all in Python


Setup
-----
* Anaconda 64-bit for Windows
* TensorFlow only recently became workable on Windows!
* CPU-only TF, ignore warnings: https://github.com/tensorflow/tensorflow/issues/7778
* Since using Anaconda prompt for TF stuff, remember `dir`, `cls`, and just typing drive letter followed by a colon to switch drives


```
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
```