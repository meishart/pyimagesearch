# Reference: https://www.pyimagesearch.com/2017/08/21/deep-learning-with-opencv/

import numpy as np
import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-l", "--labels", required=True, help="path to ImageNet labels (i.e., syn-sets)")

args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])

# load class labels from disk
rows = open(args["labels"]).read().strip().split("\n")
classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

# cnn requires image to be of size 224x224 pixels
blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

# load serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# perform forward-pass to obtain classfication on the blob
net.setInput(blob)
start = time.time()
preds = net.forward()
end = time.time()
print("[INFO] classifiction took {:.5} seconds".format(end - start))

# sort the indexes of the probabilities in descending order (higher
# probabilitiy first) and grab the top-5 predictions
indexes = np.argsort(preds[0])[::-1][:5]

# display the top 5 predictions
for (i, idx) in enumerate(indexes):
    print("[INFO] {}. label: {}, probability: {:.5}".format(i+1, classes[idx], preds[0][idx]))

# display output image
cv2.imshow("image", image)
cv2.waitKey(0)
