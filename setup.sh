#!/bin/bash

set -o errexit

sudo apt-get install git gdal-bin python-gdal
#sudo pip install requests
#sudo pip install boto

if [ ! -d usgs ] ; then
  git clone git@github.com:mapbox/usgs.git
  (cd usgs; sudo python setup.py install)
fi


