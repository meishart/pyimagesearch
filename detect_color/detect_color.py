# PyImageSearch: Color detection in an image
# Reference: https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/


import numpy as np
import argparse
import cv2
import imutils

# construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "path to the image")
ap.add_argument("-c", "--color", required=True, help = "color to be detected")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
(h,w,d) = image.shape
print("Width:{}, Height:{}, Depth:{}".format(w,h,d))

# color to be detected
color = args["color"]
print("Color to be detected- {}".format(color))

# Enable to view RGB value for each array on mouse hover.
# cv2.imshow("image", image)
# cv2.waitKey(0)

# define the list of boundaries for colors - red, blue, yellow & gray
# Each entry in the tuple contains [B, G, R]
boundaries = {
    'red': {
        'lower': [1, 1, 180],
        'upper': [10, 10, 230]
    },
    'yellow': {
        'lower': [85, 185, 230],
        'upper': [105, 205, 255]
    },
    'blue': {
        'lower': [70, 35, 1],
        'upper': [100, 55, 10]
    },
    'gray': {
        'lower': [120, 120, 120],
        'upper': [150, 150, 150]
    }
}

# Prepare and apply mask
lower = np.array(boundaries[color]['lower'], dtype = "uint8")
upper = np.array(boundaries[color]['upper'], dtype = "uint8")

mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask=mask)

# Render masked image
cv2.imshow("images", np.hstack([image, output]))
cv2.waitKey(0)
