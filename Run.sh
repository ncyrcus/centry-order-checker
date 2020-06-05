#!/bin/bash -e
# 
docker build -t revisorgl .
full_path=$(realpath $0)
SCRIPTPATH=$(dirname $full_path)
docker run -it --rm --name microservicio -v $SCRIPTPATH/script-log/:/usr/src/app/log/ revisorgl