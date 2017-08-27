#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 09:30:00 2017

@author: German
"""

# PARTE 1 - HACER LA CNN
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Conv2D
from keras.models import model_from_json
import os
import keras as k

k.__version__


from keras.preprocessing.image import ImageDataGenerator

#Preprocessing images

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)


training_set = train_datagen.flow_from_directory('data_set',
                                                target_size=(64, 64),
                                                batch_size=32,
                                                class_mode='binary')

test_set = test_datagen.flow_from_directory('data_set',
                                            target_size=(64, 64),
                                            batch_size=32,
                                            class_mode='binary')




num_classes = test_set.num_class

# Haz la CNN 
classifier = Sequential()
classifier.add(Conv2D(64, (3,3), input_shape = (64,64,3), activation = "relu", data_format = 'channels_last'))
classifier.add(MaxPooling2D(pool_size = (2,2)))
classifier.add(Conv2D(64,  (3,3), activation = "relu"))
classifier.add(MaxPooling2D(pool_size = (2,2))) 
classifier.add(Conv2D(64,  (3,3), activation = "relu"))
classifier.add(MaxPooling2D(pool_size = (2,2))) 

classifier.add(Flatten())   #La matriz de la imagen la conviertes en un vector (segun yo verdad)

classifier.add(Dense(output_dim = 128, activation = "relu"))
classifier.add(Dropout(0.5))
classifier.add(Dense(output_dim = 128, activation = "relu"))
classifier.add(Dropout(0.5))

classifier.add(Dense(output_dim = num_classes, activation = "softmax"))

#Compila el classifier, arriba lo estas haciendo, abajo lo compilas
classifier.compile(optimizer = "rmsprop", loss = "categorical_crossentropy", metrics = ["accuracy"])


# PARTE 2 - YA TIENES LA CNN HECHA Y COMPILADA
#           AHORA VAS A ENTRENARLA CON LAS IMAGENES

classifier.fit_generator(training_set,
                    steps_per_epoch=75000 / 64,
                    epochs=25,
                    validation_data=test_set,
                    validation_steps=25000/32)


#PARTE 2.5 - ASI GUARDAMOS EL MODELO EN JSON
model_json = classifier.to_json()
with open("classifier.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
classifier.save_weights("model.h5")
print("Saved model to disk")

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

loaded_model.layers[0].input_shape = (64,64,3)

import coremltools
cml = coremltools.converters.keras.convert(('model.json', 'model.h5'), image_input_names='image_input', is_bgr = True)
####
#
#coremltools.converters.keras.convert(model, input_names=None, output_names=None, 
#image_input_names=None, is_bgr=False, red_bias=0.0, green_bias=0.0, blue_bias=0.0,
#gray_bias=0.0, image_scale=1.0, class_labels=None, predicted_feature_name=None)
####
