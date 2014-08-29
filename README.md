# REST Services in Bash

This is some example code I worked up to demonstrate a couple of points about HTTP and REST services: First, that they're fundamentally pretty simple, and second, and somewhat in contrast, the HTTP protocol has a lot of richness to it, which lets you do some pretty cool stuff.

## Installation

You need to have bash installed and apache configured to let you run CGI scripts. The `master` branch should run on any flavor of Linux. Check out the `osx` branch if you want to run this on a Mac. (The README in that branch has additional setup instructions.)

Clone this project to any directory you're allowed to run CGI scripts from.

## The Services

There are two services implemented in these examples: `load`, which reports the Unix system load averages, and `status`, which lets you set and check a status (one of `GREEN`, `YELLOW`, or `RED`).

In the URLs below, `$BASE_URL` stands in for the part of the URL that is specific to where you installed the scripts. (For me, it's `http://localhost/~colin/`).

### Version 1

`load` is about the simplest web service imaginable. It just sets the `Content-Type` header and dumps the output from `uptime`.

```
curl -si $BASE_URL/api/v1/load/
```

`status` is a bit more sophisticated. It lets you GET the current status or PUT a new status. PUT returns 204 (no content) on success, and 400 if the request entity is anything other than GREEN, YELLOW, or RED.

```
curl -si $BASE_URL/api/v1/status/
curl -si -X PUT -d YELLOW $BASE_URL/api/v1/status/
```

### Version 2

This version adds API documentation. Depending on the `Accept` header, the API calls will return either documentation (`text/plain` or `text/html`) or the requested resource (`application/json`).

```
curl -si $BASE_URL/api/v2/load/
curl -si -H 'Accept: text/html' $BASE_URL/api/v2/load/
curl -si -H 'Accept: application/json' $BASE_URL/api/v2/load/
```
```
curl -si $BASE_URL/api/v2/status/
curl -si -H 'Accept: text/html' $BASE_URL/api/v2/status/
curl -si -H 'Accept: application/json' $BASE_URL/api/v2/status/
curl -si -X PUT -d RED $BASE_URL/api/v2/status/
```

### Version 3

This version adds response caching to `status`. GET responses now include an `ETag` header (a sha1 digest of the status code). If that value is included as a `If-None-Match` header in later requests, you'll get a 304 response as long as the status remains unchanged.

```
curl -si -H "Accept: application/json" $BASE_URL/api/v3/status/
curl -si -H "Accept: application/json" -H "If-None-Match: 620e41f9a45c62acb7b0ef0566b4e9ac911f4244" $BASE_URL/api/v3/status/
```

In `load`, we add API documentation in German, which you can request with the `Accept-Language` header.

```
curl -si -H "Accept-Language: de" $BASE_URL/api/v3/load/
curl -si -H "Accept: text/html" -H "Accept-Language: de" $BASE_URL/api/v3/load/
```

## Example session

```
$ curl -si $BASE_URL/api/v1/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

 14:35:38 up 1 day,  8:23,  5 users,  load average: 0.38, 0.30, 0.22
```
```
$  curl -si $BASE_URL/api/v1/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 4
Content-Type: text/plain

RED
```
```
$  curl -si -X PUT -d YELLOW $BASE_URL/api/v1/status/
HTTP/1.1 204 No Content
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 0
Content-Type: text/plain

```
```
$  curl -si $BASE_URL/api/v2/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

LOAD
The 'load' resource contains the unix system load information for this server.
GET is the only valid method.
Data is returned as application/json.
```
```
$  curl -si -H 'Accept: text/html' $BASE_URL/api/v2/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/html

<h1><code>load</code></h1>
<p>The 'load' resource contains the unix system load information for this server.</p>
<p><code>GET</code> is the only valid method.</p>
<p>Data is returned as <code>application/json</code>.</p>
```
```
$  curl -si -H 'Accept: application/json' $BASE_URL/api/v2/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Transfer-Encoding: chunked
Content-Type: application/json

{"load": {"1": 0.38, "5": 0.30, "15": 0.22}}
```
```
$  curl -si $BASE_URL/api/v2/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

STATUS
The 'status' resource contains the project status
GET and PUT are valid methods.
The valid status codes are GREEN, YELLOW and RED.
Data is returned as application/json.
```
```
$  curl -si -H 'Accept: text/html' $BASE_URL/api/v2/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/html

<h1><code>status</code></h1>
<p>The 'status' resource contains the project status</p>
<p><code>GET</code> and <code>PUT</code> are valid methods.</p>
<p>The valid status codes are <code>GREEN</code>, <code>YELLOW</code> and <code>RED</code>.</p>
<p>Data is returned as <code>application/json</code>.</p>
```
```
$  curl -si -H 'Accept: application/json' $BASE_URL/api/v2/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Transfer-Encoding: chunked
Content-Type: application/json

{"status": "RED"}
```
```
$  curl -si -X PUT -d RED $BASE_URL/api/v2/status/
HTTP/1.1 204 No Content
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 0
Content-Type: text/plain

```
```
$  curl -si -H "Accept: application/json" $BASE_URL/api/v3/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:35:38 GMT
Server: Apache/2.4.7 (Ubuntu)
ETag: 620e41f9a45c62acb7b0ef0566b4e9ac911f4244
Transfer-Encoding: chunked
Content-Type: application/json

{"status": "RED"}
```
```
$  curl -si -H "Accept: application/json" -H "If-None-Match: 620e41f9a45c62acb7b0ef0566b4e9ac911f4244" $BASE_URL/api/v3/status/
HTTP/1.1 304 Not Modified
Date: Mon, 18 Aug 2014 18:35:53 GMT
Server: Apache/2.4.7 (Ubuntu)

```
$ curl -si -H "Accept-Language: de" $BASE_URL/api/v3/load/
HTTP/1.1 200 OK
Date: Fri, 29 Aug 2014 23:22:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-language: de
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

LOAD
Die 'load' Ressource enth&auml;lt das Unix-System Lastinformationen f&uuml;r diesen Server.
GET ist die einzige g&uuml;ltige Methode.
Daten als application/json zur&uuml;ck.
```
```
$ curl -si -H "Accept: text/html" -H "Accept-Language: de" $BASE_URL/api/v3/load/
HTTP/1.1 200 OK
Date: Fri, 29 Aug 2014 23:22:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-language: de
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/html

<h1><code>load</code></h1>
<p>Die 'load' Ressource enth&auml;lt das Unix-System Lastinformationen f&uuml;r diesen Server.</p>
<p><code>GET</code> ist die einzige g&uuml;ltige Methode.</p>
<p>Daten als <code>application/json</code> zur&uuml;ck.</p>
```
