#!/usr/local/bin/bash

accept=${HTTP_ACCEPT,,}

# The accept header may have multiple types, so we check if it's the same with 'application/json' replaced by ''.
#     I.e. If it contains 'application/json', it won't be the same with it removed.
if [ "$accept" != "${accept/application\/json/}" ] ; then
    echo "Content-type: application/json"
    echo
    /usr/local/opt/coreutils/libexec/gnubin/uptime | /usr/local/opt/gnu-sed/libexec/gnubin/sed -r 's/^.*load average: (.*), (.*), (.*)/{"load": {"1": \1, "5": \2, "15": \3}}/;'
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
