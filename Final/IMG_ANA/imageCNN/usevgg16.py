# import the necessary packages
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K
from keras.applications import VGG16

class UseVGG16:
	@staticmethod
	def build(width, height, depth, classes, finalAct="sigmoid"):
		# initialize the model along with the input shape
		model = Sequential()
		inputShape = (height, width, depth)

		# Remove the top layer 
		conv_base = VGG16(weights='imagenet',  input_shape= inputShape, include_top=False )
		conv_base.trainable = False
		
		model.add(conv_base)

		# first (and only) set of FC => RELU layers
		model.add(Flatten())
		model.add(Dense(1024))
		model.add(Activation("relu"))
		model.add(BatchNormalization())
		model.add(Dropout(0.5))

		# sigmoid classifier
		model.add(Dense(classes))
		model.add(Activation(finalAct))

		# return the constructed network architecture
		return model