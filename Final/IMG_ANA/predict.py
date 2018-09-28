# USAGE
# python predict.py --model fashion.model --labelbin mlb.pickle --image samples/1.jpeg

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True)
ap.add_argument("-l", "--labelbin", required=True)
ap.add_argument("-i", "--image", required=True)
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
 
# pre-process the image for classification
image = cv2.resize(image, (150, 150))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network and the labels
print("[INFO] loading network...")
model = load_model(args["model"])
mlb = pickle.loads(open(args["labelbin"], "rb").read())

print("[INFO] classifying image...")
proba = model.predict(image)[0]

# Get the probabilities for each of the individual labels
for (label, p) in zip(mlb.classes_, proba):
	print("{}: {:.2f}%".format(label, p * 100))
