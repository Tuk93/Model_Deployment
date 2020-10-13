# Model_Deployment

Wearing masks in the current pandemic (COVID-19) is made mandatory by multiple countries. This is a basic resnet implementation that performs binary classification of images and identifies images where the individual is wearing a mask or not.This project can therefore be used in real-time applications which require face-mask detection for safety purposes.Hence it can be integrated with embedded systems for application in airports, railway stations, offices, schools, and public places to ensure that public safety guidelines are followed.

The model for this implementation was trained with the mask dataset from kaggle which contains images of persons with masks and without masks.

In the container directory are all the components you need to package the sample algorithm for Amazon SageMager:

.
|-- Dockerfile
|-- build_and_push.sh
`-- decision_trees
    |-- nginx.conf
    |-- predictor.py
    |-- serve
    |-- train
    `-- wsgi.py

Let's discuss each of these in turn:

    Dockerfile describes how to build your Docker container image.
    
    build_and_push.sh is a script that uses the Dockerfile to build your container images and then pushes it to ECR. We'll invoke the commands directly later in this notebook, but you can just copy and run the script for your own algorithms.
    
    decision_trees is the directory which contains the files that will be installed in the container.
    
    local_test is a directory that shows how to test your new container on any computer that can run Docker, including an Amazon SageMaker notebook instance. Using this method, you can quickly iterate using small datasets to eliminate any structural bugs before you use the container with Amazon SageMaker. 
    
    In this simple application, we only install five files in the container. You may only need that many or, if you have many supporting routines, you may wish to install more. These five show the standard structure of our Python containers, although you are free to choose a different toolset and therefore could have a different layout. If you're writing in a different programming language, you'll certainly have a different layout depending on the frameworks and tools you choose.

The files that we'll put in the container are:

    nginx.conf is the configuration file for the nginx front-end.
    
    predictor.py is the program that actually implements the Flask web server and the decision tree predictions for this app. we can further customize the actual prediction parts to your application.
    
    serve is the program started when the container is started for hosting. It simply launches the gunicorn server which runs multiple instances of the Flask app defined in predictor.py. 
    
    train is the program that is invoked when the container is run for training. You will modify this program to implement your training algorithm.
    
    wsgi.py is a small wrapper used to invoke the Flask app. You should be able to take this file as-is.
    
The images used were real images of faces wearing masks. The images were collected from the following sources:

# Kaggle datasets

# Installation and How to run this demo to test locally before deploying it into production :

1. Clone the repo
git clone https://github.com/Tuk93/Model_Deployment.git
2.Change your directory to the cloned repo.
3.First you can test the locally using local_test, to do so you can insert image url in  file predict.sh file and then build the container as below :

docker build . -t mask

docker run -p 8080:8080 --rm mask serve

cd decision tree

./predict.sh

### Now you can test the same using streamlit web app where you can insert image (jpg, png) and get the prediction from the same model.

Streamlit is an open-source Python library that makes it easy to build beautiful custom web-apps for machine learning and data science. Streamlit can be installed easily using pip. Deployment of machine learning models is the process of putting models into production so that web applications and APIs can consume a trained model and generate predictions with new data points.

pip install streamlit

Once you installed streamlit you can change the directory to the decision_trees/model/trained_weights/ where we have app_test.py simple web app classification, once you upload the image it will be saved at folder 'image/' and we will pass model_path as the image folder to get the predictions on the uploaded image.

To start the web app you need to run below command :
streamlit run app_test.py 

you will be prompted with 2 URLs : for ex 

You can now view your Streamlit app in your browser.

  Network URL: http://172.31.75.85:8501
  External URL: http://3.238.72.86:8501
  
 Please note, If you are using Ec2 instance you will need to open port 8501 to 0.0.0.0
  
  

