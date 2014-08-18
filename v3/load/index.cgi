#!/bin/bash

accept=${HTTP_ACCEPT,,}

if [ "$accept" != "${accept/application\/json/}" ] ; then
    echo "Content-type: application/json"
    echo
    uptime | sed -r 's/^.*load average: (.*), (.*), (.*)/{"load": {"1": \1, "5": \2, "15": \3}}/;'
else
    if [ "$accept" != "${accept/text\/html}" ] ; then
        echo "Content-type: text/html"
        echo
        echo "<h1><code>load</code></h1>"
        echo "<p>The 'load' resource contains the unix system load information for this server.</p>"
        echo "<p><code>GET</code> is the only valid method.</p>"
        echo "<p>Data is returned as <code>application/json</code>.</p>"
    else
        echo "Content-type: text/plain"
        echo
        echo "LOAD"
        echo "The 'load' resource contains the unix system load information for this server."
        echo "GET is the only valid method."
        echo "Data is returned as application/json."
    fi
fi