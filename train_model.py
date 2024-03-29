from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras_preprocessing import image
#from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt


# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = 'C:\\Users\\Usha Sree\\OneDrive\\Documents\\Face-Recognition\\data\\train'
valid_path = 'C:\\Users\\Usha Sree\\OneDrive\\Documents\\Face-Recognition\\data\\test'

# add preprocessing layer to the front of VGG
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg.layers:
  layer.trainable = False



folders = glob('C:\\Users\\Usha Sree\\OneDrive\\Documents\\Face-Recognition\\data\\train\\*')
print(len(folders))

# No of layers
x = Flatten()(vgg.output)
prediction = Dense(2, activation='softmax')(x)

# create a model object
model = Model(inputs=vgg.input, outputs=prediction)

# view the structure of the model
model.summary()

# Compile the model
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)


from keras_preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True,
                                   validation_split=0.2)  # specify the validation split here

# Set up the ImageDataGenerator for test data (without validation split)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('C:\\Users\\Usha Sree\\OneDrive\\Documents\\Face-Recognition\\data\\train\\ushasree',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical',
                                                 subset='training')  # specify that this is the training subset


test_set = test_datagen.flow_from_directory('C:\\Users\\Usha Sree\\OneDrive\\Documents\\Face-Recognition\\data\\test\\ushasree',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')
                                           
print(len(training_set))

print(len(test_set)) 

# fit the model
r = model.fit(
  training_set,
  validation_data=test_set,
  epochs=2,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

'''# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# accuracies
plt.plot(r.history['acc'], label='train acc')
plt.plot(r.history['val_acc'], label='val acc')
plt.legend()
plt.show() 
plt.savefig('AccVal_acc')'''

import tensorflow as tf

from keras.models import load_model

##Saving the model
model.save('final_model.keras')
