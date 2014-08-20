#!/usr/local/bin/bash

dir=`dirname $0`
filename=$dir/status.txt
status=`cat $filename`

method=${REQUEST_METHOD^^}

if [ "$method" == "GET" ] ; then
    echo "Content-type: text/plain"
    echo
    echo "$status"
else
    if [ "$method" == "PUT" ] ; then
        read -n $CONTENT_LENGTH status
        status=${status^^}
        if [ "$status" == "GREEN" ] || [ "$status" == "YELLOW" ] || [ "$status" == "RED" ] ; then
            echo "$status" > $filename
            echo "Content-type: text/plain"
            echo "Status: 204"
            echo
        else
            echo "Content-type: text/plain"
            echo "Status: 400"
            echo
            echo "Invalid status code"
        fi
    fi
fi
