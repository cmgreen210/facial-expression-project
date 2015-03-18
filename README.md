# Facial Expression Classification Web App | :smile: :frowning: :open_mouth:
Chris Green, March 2015

##Contents
* [TL;DR](#tldr)
* [Overview](#overview)
* [Model](#model)
* [Web App](#app)
* [Installation](#install)

<a name="tldr"/>
##TL;DR
This Django project classifies a person's face as either happy, sad, or surprised. The live web-app can be found [here][1]. The convolutional neural network training code and documentation can be found in [this repo][2].

![Home Page](https://github.com/cmgreen210/facial-expression-project/blob/master/img/page.png)

<a name="overview"/>
##Overview
Can we teach a machine to recognize human emotions? That was the question I wanted to tackle in my capstone project for [Zipfian Academy's][4] winter 2015 data science cohort. Luckily I found a large dataset of labeled grayscale images of faces broken into 7 different classes [here][5]. For modeling I choose to experiment with [convolutional neural networks][6], a type of deep learning model especially suited for image recognition. Training using all 7 labels proved challenging so I reduced the problem down to 3 expression: Happy, Sad, and Surprised. Even with this reduction in scope we still had ~19,000 images to work with. The final model was able to acheive 75% accuracy.

<a name="model"/>
##Model
A detailed overview of the facial expression classification package used in this app can be found [here][1].

<a name="app"/>
##Web App

<a name="install"/>
##Installation

[1]: http://www.fec.space "Web App"
[2]: https://github.com/cmgreen210/facial-expression-classifier "FEC Repo"
[3]: https://www.djangoproject.com/ "Django site"
[4]: http://www.zipfianacademy.com/ "Zipfian"
[5]: https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data "Data"
[6]: http://en.wikipedia.org/wiki/Convolutional_neural_network "CNN"
