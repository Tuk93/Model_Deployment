import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
from shutil import copyfile
import sys
import signal
import traceback
import requests
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model,model_from_json
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras_preprocessing.image import ImageDataGenerator
import numpy
import os
import shutil # to save it locally
import flask
import pandas as pd
def predict(model, model_path):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        
        print('debug here 1')
        image_size = 224
        data_generator = ImageDataGenerator(preprocessing_function=preprocess_input,horizontal_flip=True,
                                               width_shift_range = 0.2,
                                               height_shift_range = 0.2)
        test_gen1=data_generator.flow_from_directory('image/',target_size=(image_size, image_size),
                    class_mode='categorical',shuffle=False)
        predictions_test=model.predict_generator(test_gen1)
        print('debug here 2')
        print(len(predictions_test))
        res_test=[]
        
        for i in predictions_test:
            print(i[0])
            if i[0]<0.5:
                res_test.append("Not Wearing mask")
            else:
                res_test.append("Wearing mask")
        print(res_test)
        return res_test
     

def get_model():
        """Get the model object for this instance, loading it if it's not already loaded."""
        json_file = open('working_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
        loaded_model.load_weights('working_model.h5')
        print("Loaded model from disk")

        loaded_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

        return loaded_model

st.write("""
         # Mask Detection
         """
         )

st.write("This is a simple image classification web app ")

file = st.file_uploader("Please upload an image file", type=["jpg", "png"])
print(file)
if file is None:
    st.text("You haven't uploaded an image file")
else:
    image = Image.open(file)
    image=image.save('image/image1.jpg')
    model_path='image/image1.jpg'
    
    model=get_model()
    st.image(model_path, use_column_width=True)
    prediction = predict(model,model_path)
    
    if np.argmax(prediction) == 0:
        st.write("Person Wearing Mask!")
    else:
        st.write("Person Without Mask!")
    
    st.text("Probability(0: with_mask, 1: without_mask)")
    st.write(prediction)
