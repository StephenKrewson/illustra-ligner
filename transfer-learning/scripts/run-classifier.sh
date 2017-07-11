#!/bin/bash

find $1 -name '*.jpg' | while read file; do python classify_image_mk.py --image_file $file; done
