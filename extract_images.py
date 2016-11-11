import argparse
import cv2
import numpy as np
import os
from random import shuffle

# bounds for side length in pixels of image
LOW_BOUND = 100

# threshold for overlap to remove image
OVERLAP_FRACTION = 0.3


class BoundingBox:
    def overlaps(self, abbox):
        x_condition = self.x1 < abbox.x0 or abbox.x1 < self.x0
        y_condition = self.y1 < abbox.y0 or abbox.y1 < self.y0
        if x_condition and y_condition:
            return False
        return True

    def __str__(self):
        return "((%d, %d), (%d, %d))" % (self.x0, self.y0, self.x1, self.y1)

    def __repr__(self):
        return "((%d, %d), (%d, %d))" % (self.x0, self.y0, self.x1, self.y1)

    def slice_image(self, img):
        return img[self.y0:self.y1, self.x0:self.x1]

    def meets_low_bound(self, low_bound):
        x_condition = self.x1 - self.x0 > low_bound
        y_condition = self.y1 - self.y0 > low_bound
        return x_condition and y_condition

    def expand_by_bbox(self, abbox):
        self.x0 = min(self.x0, abbox.x0)
        self.y0 = min(self.y0, abbox.y0)
        self.x1 = max(self.x1, abbox.x1)
        self.y1 = max(self.y1, abbox.y1)
        self.area = (self.y1 - self.y0) * (self.x1 - self.x0)

    def __init__(self, x, y, w, h):
        self.x0 = x
        self.y0 = y
        self.x1 = x + w
        self.y1 = y + h
        self.area = w * h


def combine_rectangles(rectangles):
    did_combine = True
    while did_combine:
        did_combine = False
        will_remove = []
        for i in range(len(rectangles)):
            for j in range(i):
                if rectangles[i].overlaps(rectangles[j]):
                    rectangles[j].expand_by_bbox(rectangles[i])
                    did_combine = True
                    will_remove.append(i)
        for index in sorted(list(set(will_remove)), reverse=True):
            rectangles.pop(index)


def bounding_boxes_for_image(image_path):
    img = cv2.imread(image_path, 0)
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    rectangles = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < LOW_BOUND or h < LOW_BOUND or (x == 1 and y == 1):
            continue
        rectangles.append(BoundingBox(x, y, w, h))

    combine_rectangles(rectangles)
    # filter out rectangles that are below the low bound
    rectangles = filter(lambda x: x.meets_low_bound(LOW_BOUND), rectangles)
    return img, rectangles


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default='')
    parser.add_argument('--image_dir', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='')
    parser.add_argument('--low_bound', type=int, default=200)
    parser.add_argument('--overlap', type=float, default=0.8)
    args = parser.parse_args()

    if not args.image_path and not args.image_dir:
        print('Please provide an image_path or an image_dir')
        exit(1)

    image_paths = []
    prefixes = []
    if args.image_dir:
        filenames = os.listdir(args.image_dir)
        for filename in filenames:
            image_paths.append(os.path.join(args.image_dir, filename))
            prefixes.append(filename.split('.')[0])
    else:
        image_paths.append(args.image_path)
        prefixes.append(args.image_path.split('.')[0])

    LOW_BOUND = args.low_bound
    OVERLAP_FRACTION = args.overlap

    for prefix, image_path in zip(prefixes, image_paths):
        img, bboxes = bounding_boxes_for_image(image_path)
        for i, large in enumerate(bboxes):
            illustration = large.slice_image(img)
            if not args.output_dir:
                cv2.imshow("illustration %d" % (i), illustration)
                cv2.waitKey(0)
            else:
                outpath = os.path.join(args.output_dir,
                                       "%s_ex_%d.jpg" % (prefix, i))
                cv2.imwrite(outpath, illustration)
