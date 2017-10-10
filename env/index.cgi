#!/bin/bash

echo 'Content-type: text/plain'
echo

env | sort
if [[ $CONTENT_LENGTH > 0 ]] ; then
    read -n $CONTENT_LENGTH content
    echo '-------------------- content --------------------'
    echo "$content"
fi
