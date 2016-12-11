The classify_image_mk.py is a fork of https://github.com/tensorflow/tensorflow/blob/master/tensorflow/models/image/imagenet/classify_image.py

following the ideas in:

http://stackoverflow.com/questions/34809795/tensorflow-return-similar-images

I ran the classify_image_mk.py script on all 28,000 images by using:

find <imagedirectory> -name '*.jpg' | while read file; do python classify_image_mk.py --image_file $file; done


--
Other notes:
https://indico.io/blog/clothing-similarity-how-a-program-is-more-fashionable-than-me/
(refrences a comercial API, but method is interesting)

Generating fake images:
https://bamos.github.io/2016/08/09/deep-completion/

Interesting write-up of competing tools:
https://github.com/zer0n/deepframeworks/blob/master/README.md

I just realized you need this too! The vector creation utility is in code, and the nearest neighbors / dimension reduciton are in image-vectors. All of this was done very quickly on a Friday, so no promises! 

	  print('%s (score = %.5f)' % (human_string, score))