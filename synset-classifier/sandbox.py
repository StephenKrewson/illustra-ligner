import os
import sys


if __name__ == '__main__':

	if len(sys.argv) != 3:
		print('USAGE: python classify_image_mk.py <INPUT_DIR> <OUTPUT_DIR>')

	# Save the 
	images = os.path.abspath(sys.argv[1])
	outdir = os.path.abspath(sys.argv[2])
	
	