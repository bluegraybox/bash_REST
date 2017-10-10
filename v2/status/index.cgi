#!/usr/local/bin/bash

export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"

dir=`dirname $0`
filename=$dir/status.txt

method=${REQUEST_METHOD^^}

if [ "$method" == "GET" ] ; then
    accept=${HTTP_ACCEPT,,}  # lowercase
    # $accept may have multiple content types, so we can't do an exact match.
    # Does $accept contain 'application/json'?
    if [ -z ${accept##*application/json*} ] ; then
        status=`cat $filename`
        echo "Content-type: application/json"
        echo
        echo '{"status": "'$status'"}'
    else
        if [ -z ${accept##*text/html*} ] ; then
            echo "Content-type: text/html"
            echo
            echo "<h1><code>status</code></h1>"
            echo "<p>The 'status' resource contains the project status</p>"
            echo "<p><code>GET</code> and <code>PUT</code> are valid methods.</p>"
            echo "<p>The valid status codes are <code>GREEN</code>, <code>YELLOW</code> and <code>RED</code>.</p>"
            echo "<p>Data is returned as <code>application/json</code>.</p>"
        else
            echo "Content-type: text/plain"
            echo
            echo "STATUS"
            echo "The 'status' resource contains the project status"
            echo "GET and PUT are valid methods."
            echo "The valid status codes are GREEN, YELLOW and RED."
            echo "Data is returned as application/json."
            echo "Accept: '$accept'"
        fi
    fi
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
