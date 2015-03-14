from distutils.core import setup

setup(
    # Application name:
    name="Django Facial Expression Classifier App",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Chris Green",
    author_email="cmgreen210@gmail.com",

    # Packages
    packages=["django_expression"],

    # Include package data
    package_data = {
        'django_expression': ['static/django_expression/css/*',
                              'static/django_expression/fonts/*',
                              'static/django_expression/image/*',
                              'static/django_expression/js/*',
                              'templates/django_expression/*'],
    },

    # Details
    url="https://github.com/cmgreen210/face-django_expression-classifier",

    #
    # license="LICENSE.txt",
    description="Django app for facial django_expression "
                "classification from images and video",

    long_description=open("README.md").read(),
)
