#!/bin/sh
sudo apt-get update

# CUDA
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1204/x86_64/cuda-repo-ubuntu1204_6.5-14_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1204_6.5-14_amd64.deb
sudo apt-get update
sudo apt-get install -y cuda

# PYTHON STUFF
sudo apt-get install python-setuptools
sudo easy_install pip
sudo apt-get install python

# GRAPHLAB
sudo pip install http://static.dato.com/files/graphlab-create-1.3.gpu.tar.gz
