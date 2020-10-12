# Model_Deployment

Wearing masks in the current pandemic (COVID-19) is made mandatory by multiple countries. This is a basic resnet implementation that performs binary classification of images and identifies images where the individual is wearing a mask or not.

The model for is implementation was trained with the mask dataset from kaggle which contains images of persons with masks and without masks.

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
    
    local_test is a directory that shows how to test your new container on any computer that can run Docker, including an Amazon SageMaker notebook instance. Using this method, you can quickly iterate using small datasets to eliminate any structural bugs before you use the container with Amazon SageMaker. We'll walk through local testing later in this note
    
    In this simple application, we only install five files in the container. You may only need that many or, if you have many supporting routines, you may wish to install more. These five show the standard structure of our Python containers, although you are free to choose a different toolset and therefore could have a different layout. If you're writing in a different programming language, you'll certainly have a different layout depending on the frameworks and tools you choose.

The files that we'll put in the container are:

    nginx.conf is the configuration file for the nginx front-end.
    
    predictor.py is the program that actually implements the Flask web server and the decision tree predictions for this app. we can further customize the actual prediction parts to your application.
    
    serve is the program started when the container is started for hosting. It simply launches the gunicorn server which runs multiple instances of the Flask app defined in predictor.py. 
    
    train is the program that is invoked when the container is run for training. You will modify this program to implement your training algorithm.
    
    wsgi.py is a small wrapper used to invoke the Flask app. You should be able to take this file as-is.

How to run this demo to test locally first before production :

docker build . -t mask

docker run -p 8080:8080 --rm mask serve

cd decision tree

./predict.sh
