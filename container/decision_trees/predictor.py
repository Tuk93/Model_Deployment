# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import json
import pickle
import io 
import sys
import signal
import traceback
import requests
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

prefix = '/opt/program/'
model_path = os.path.join(prefix, 'model')

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.
def download_image(image_url):
    image_name=image_url.split("/")[-1]
    extention=image_name.split('.')[-1]
    filename = model_path+'/image/test/image.'+extention
    print(filename)
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)
    # Check if the image was retrieved successfully
    print('code '+str(r.status_code ))
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        print('hello')
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        

        print('Image sucessfully Downloaded: ',filename)
        #shutil.move(image_name,filename)
    else:
        print('Image Couldn\'t be retreived')
        
class ScoringService(object):
    model = None                # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            # load json and create model
            json_file = open(model_path+'/trained_weights/working_model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights(model_path+'/trained_weights/working_model.h5')
            print("Loaded model from disk")

            loaded_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
            cls.model=loaded_model
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model()
        download_image(input)
                
        print('debug here 1')
        image_size = 224
        data_generator = ImageDataGenerator(preprocessing_function=preprocess_input,horizontal_flip=True,
                                               width_shift_range = 0.2,
                                               height_shift_range = 0.2)
        test_gen1=data_generator.flow_from_directory(model_path+'/image/',target_size=(image_size, image_size),
                    class_mode='categorical',shuffle=False)
        predictions_test=clf.predict_generator(test_gen1)
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
        #return clf.predict(input)

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == 'application/json':
        data = flask.request.data.decode('utf-8')
        print(data)
        #print(type(data))
        json_data=json.loads(data)
        
        print(json_data['url'])
        #data = pd.read_csv(s, header=None)
    else:
        return flask.Response(response='This predictor only supports json data', status=415, mimetype='text/plain')

    print('Invoked with {} '.format(json_data))

    # Do the prediction
    predictions = ScoringService.predict(json_data['url'])

    # Convert from numpy back to CSV
    out = io.StringIO()
    pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype='text/csv')
