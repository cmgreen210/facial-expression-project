#!/bin/sh

sudo yum groupinstall "Development tools"
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz # Download
tar xvfz Python-2.7.3.tgz # unzip
cd Python-2.7.3 # go into directory
./configure
sudo make # build
sudo make altinstall

cd ~

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py

sudo python2.7 ez_setup.py
sudo easy_install-2.7 pip
