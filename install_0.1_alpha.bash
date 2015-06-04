#!/bin/bash

cd /opt/
wget https://github.com/wtelecom/net-interviewer/archive/net-interviewer_0.1.tar.gz
tar -xf net-interviewer_0.1.tar.gz
sudo apt-get install virtualenv

cd net-interviewer-net-interviewer_0.1
virtualenv ./env
source ./env/bin/activate

#python src/net-interviewer.py -c net_interviewer.conf
