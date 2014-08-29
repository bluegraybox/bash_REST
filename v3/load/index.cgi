#!/bin/bash

accept=${HTTP_ACCEPT,,}
language=${HTTP_ACCEPT_LANGUAGE,,}
language=${language:0:2}

if [ "$accept" != "${accept/application\/json/}" ] ; then
    echo "Content-type: application/json"
    echo
    uptime | sed -r 's/^.*load average: (.*), (.*), (.*)/{"load": {"1": \1, "5": \2, "15": \3}}/;'
else
    if [ "$language" == "de" ] ; then
        if [ "$accept" != "${accept/text\/html}" ] ; then
            echo "Content-type: text/html"
            echo "Content-language: de"
            echo
            echo "<h1><code>load</code></h1>"
            echo "<p>Die 'load' Ressource enth&auml;lt das Unix-System Lastinformationen f&uuml;r diesen Server.</p>"
            echo "<p><code>GET</code> ist die einzige g&uuml;ltige Methode.</p>"
            echo "<p>Daten als <code>application/json</code> zur&uuml;ck.</p>"
        else
            echo "Content-type: text/plain"
            echo "Content-language: de"
            echo
            echo "LOAD"
            echo "Die 'load' Ressource enthält das Unix-System Lastinformationen für diesen Server."
            echo "GET ist die einzige gültige Methode."
            echo "Daten als application/json zurück."
        fi
    else
        if [ "$accept" != "${accept/text\/html}" ] ; then
            echo "Content-type: text/html"
            echo "Content-language: en"
            echo
            echo "<h1><code>load</code></h1>"
            echo "<p>The 'load' resource contains the unix system load information for this server.</p>"
            echo "<p><code>GET</code> is the only valid method.</p>"
            echo "<p>Data is returned as <code>application/json</code>.</p>"
        else
            echo "Content-type: text/plain"
            echo "Content-language: en"
            echo
            echo "LOAD"
            echo "The 'load' resource contains the unix system load information for this server."
            echo "GET is the only valid method."
            echo "Data is returned as application/json."
        fi
    fi
fi
