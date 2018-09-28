# USAGE
# python train.py --dataset data/train_images --file input/train.json --model fashion.model --labelbin mlb.pickle

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MultiLabelBinarizer
from imageCNN.usevgg16 import UseVGG16
from imutils import paths
import numpy as np
import argparse
import random
import pickle
import cv2
import os
import json
from pandas.io.json import json_normalize
import sys
import gc

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset (i.e., directory of images)")
ap.add_argument("-f", "--file", required=True,
	help="path to input label json file (i.e., json of images, labels)")
ap.add_argument("-m", "--model", required=True,
	help="path to output model")
ap.add_argument("-l", "--labelbin", required=True,
	help="path to output label binarizer")
args = vars(ap.parse_args())

# initialize the number of epochs to train for, initial learning rate,
# batch size, and image dimensions
EPOCHS = 3
INIT_LR = 1e-3
BS = 64
IMAGE_DIMS = (150, 150, 3)

# grab the image paths and randomly shuffle them
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# process json annotation dictionary
oriJSON = json.load(open( args["file"] ))
ori_label = json_normalize(oriJSON["annotations"])
labeldist = {}
setLis = set()
for i in range( len( ori_label) ):
	lis = ori_label.loc[i]['labelId']
	imgId = ori_label.loc[i]['imageId']
	labeldist[imgId] = lis
	setLis = setLis | set(lis)

# binarize the labels using scikit-learn's special multi-label
# binarizer implementation: one-hot encoding the label
# Initiate with a set of classes
mlb = MultiLabelBinarizer(classes = list(setLis))
mlb.fit_transform([("1", "2"), ("3","4"),("5",)]) # lazy evaulation. need to init first. Otherwise, problematic.

print("[INFO] compiling model...")
model = UseVGG16.build(
	width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
	depth=IMAGE_DIMS[2], classes=len(mlb.classes_),
	finalAct="sigmoid")

# initialize the optimizer (SGD is sufficient)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)  #learning rate = INIT_LR = 1e-3

# compile the model using binary cross-entropy
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
	  
def getImgs(files):
#	Need to manipulate the images here later -- shake , shift, rotation, flip.., etc.
	chunkdata = []
	for imagePath in files:
		# load the image, pre-process it, and store it in the data list
		image = cv2.imread(imagePath)
		image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
		image = img_to_array(image)
		chunkdata.append(image)
	# scale the raw pixel intensities to the range [0, 1]
	chunkdata = np.array(chunkdata, dtype="float") / 255.0
	return chunkdata

def getLabels(files):
	chunklabels = []
	for imagePath in files:
		# extract set of class labels from the image path and update the labels list
		imgId = imagePath.split(os.path.sep)[-1].split(".")[0]
		l = labeldist[imgId]
		chunklabels.append(l)
	chunklabels = np.array(chunklabels)
	chunklabels = mlb.fit_transform(chunklabels)
	return chunklabels
	
def imageLoader(files, batch_size):
	L = len(files)
	while 1:
		batch_start = 0
		batch_end = batch_size
		while batch_start < L:
			limit = min(batch_end, L)
			X = getImgs(files[batch_start:limit])
			Y = getLabels(files[batch_start:limit])
			yield (X, Y) #a tuple with two numpy arrays with batch_size samples
			del (X, Y) 
			gc.collect()    
			batch_start += batch_size   
			batch_end += batch_size

# train the network
print("[INFO] training network...")
imglab_gen = imageLoader(imagePaths, batch_size = BS )
model.fit_generator(  imglab_gen , steps_per_epoch= len(imagePaths) // BS, epochs=EPOCHS, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save( args["model"] )

# save the multi-label binarizer to disk
print("[INFO] serializing label binarizer...")
f = open( args["labelbin"] , "wb")
f.write(pickle.dumps(mlb))
f.close()


	
	