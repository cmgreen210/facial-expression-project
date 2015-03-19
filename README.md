# Facial Expression Classification Web App 

Chris Green, March 2015 :smile: :frowning: :open_mouth:

##Contents
* [TL;DR](#tldr)
* [Overview](#overview)
* [Web App](#app)
* [Model](#model)
* [Installation](#install)

<a name="tldr"/>
##TL;DR
This Django project classifies a person's face as either happy, sad, or surprised. The live web-app can be found [here][1]. The convolutional neural network training code and documentation can be found in [this repo][2].

![Home Page](https://github.com/cmgreen210/facial-expression-project/blob/master/img/page.png)

<a name="overview"/>
##Overview
Can we teach a machine to recognize human emotions? That was the question I wanted to tackle in my capstone project for [Zipfian Academy's][4] winter 2015 data science cohort. Luckily I found a large dataset of labeled grayscale images of faces broken into 7 different classes [here][5]. For modeling I choose to experiment with [convolutional neural networks][6], a type of deep learning model especially suited for image recognition. Training using all 7 labels proved challenging so I reduced the problem down to 3 expression: Happy, Sad, and Surprised. Even with this reduction in scope we still had ~19,000 images to work with. The final model was able to acheive 75% accuracy.

<a name="app"/>
##Web App
This [Django][3] project creates a site to showcase the [facial expression classifier][2] package by loading in images from the the web and classifying them. To use the site simply add a url of an image with a face in it and see what you get. Be sure to make sure it is a valid and accessible image. For example submitting this [url](http://images.sodahead.com/polls/003482687/2111968424_sad_mitt_romney_face_answer_1_xlarge.jpeg) gives:

![sad](https://github.com/cmgreen210/facial-expression-project/blob/master/img/romney.png)


<a name="model"/>
##Model
A detailed overview of the facial expression classification package used in this app can be found [here][2].

<a name="install"/>
##Installation
To install and run this app you will need register for [GraphLab Create][7] (Don't worry...it's free). You also need to install [OpenCV][8]. After installing GraphLab and OpenCV run the following bash commands:
```bash
git clone https://github.com/cmgreen210/facial-expression-project
cd facial-expression-project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
open http://127.0.0.1:8000/
```

[1]: http://www.fec.space "Web App"
[2]: https://github.com/cmgreen210/facial-expression-classifier "FEC Repo"
[3]: https://www.djangoproject.com/ "Django site"
[4]: http://www.zipfianacademy.com/ "Zipfian"
[5]: https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data "Data"
[6]: http://en.wikipedia.org/wiki/Convolutional_neural_network "CNN"
[7]: https://dato.com/products/create/quick-start-guide.html "GraphLab"
[8]: http://www.opencv.org "OpenCV"
