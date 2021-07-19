#!/bin/bash

file=$1

if [ -r ${file} ]; then
    echo ${file}
    cat ${file} | egrep -v '^$|^;|^#'
else echo "The file ${file} is not accessible"
fi
