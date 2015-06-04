#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

IP_ADDRESS="$1"

cd /opt/net-interviewer/src
source ../bin/activate

python net-interviewer.py -c $1



