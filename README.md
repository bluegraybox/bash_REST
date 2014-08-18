# REST Services in Bash

This is some example code I worked up to demonstrate a couple of points about HTTP and REST services: First, that they're fundamentally pretty simple, and second, and somewhat in contrast, the HTTP protocol has a lot of richness to it, which lets you do some pretty cool stuff.

## Installation

You need to have bash installed and apache configured to let you run CGI scripts. I've only run them on Linux, but they probably work on OS X too.

Clone this project to any directory you're allowed to run CGI scripts from.

## The Services

There are two services implemented in these examples: `load`, which reports the Unix system load averages, and `status`, which lets you set and check a status (one of GREEN, YELLOW, or RED).

In the URLs below, `$BASE_URL` stands in for the part of the URL that is specific to where you installed the scripts. (For me, it's `http://localhost/~colin/`.

### Version 1

`load` is about the simplest web service imaginable. It just sets the Content-Type header and dumps the output from `uptime`.

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
curl -si $BASE_URL/api/v1/load/
curl -si -H 'Accept: text/html' $BASE_URL/api/v1/load/
curl -si -H 'Accept: application/json' $BASE_URL/api/v1/load/
```
```
curl -si $BASE_URL/api/v1/status/
curl -si -H 'Accept: text/html' $BASE_URL/api/v1/status/
curl -si -H 'Accept: application/json' $BASE_URL/api/v1/status/
curl -si -X PUT -d RED $BASE_URL/api/v1/status/
```

### Version 3

This version adds response cacheing to `status`. GET responses now include an `ETag` header (a sha1 digest of the status code). If that value is included as a `If-None-Match` header in later requests, you'll get a 304 response as long as the status remains unchanged.

```
curl -si -H "Accept: application/json" http://localhost/~colin/api/v3/status/
curl -si -H "Accept: application/json" -H "If-None-Match: 620e41f9a45c62acb7b0ef0566b4e9ac911f4244" http://localhost/~colin/api/v3/status/
```

## Example session

```
$ curl -si $BASE_URL/api/v1/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

 14:27:21 up 1 day,  8:14,  5 users,  load average: 0.16, 0.13, 0.15
$ curl -si $BASE_URL/api/v1/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 4
Content-Type: text/plain

RED
$ curl -si -X PUT -d YELLOW $BASE_URL/api/v1/status/
HTTP/1.1 204 No Content
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 0
Content-Type: text/plain

$ curl -si $BASE_URL/api/v1/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

 14:27:21 up 1 day,  8:14,  5 users,  load average: 0.16, 0.13, 0.15
$ curl -si -H 'Accept: text/html' $BASE_URL/api/v1/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

 14:27:21 up 1 day,  8:14,  5 users,  load average: 0.16, 0.13, 0.15
$ curl -si -H 'Accept: application/json' $BASE_URL/api/v1/load/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/plain

 14:27:21 up 1 day,  8:14,  5 users,  load average: 0.16, 0.13, 0.15
$ curl -si $BASE_URL/api/v1/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 4
Content-Type: text/plain

RED
$ curl -si -H 'Accept: text/html' $BASE_URL/api/v1/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:21 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 4
Content-Type: text/plain

RED
$ curl -si -H 'Accept: application/json' $BASE_URL/api/v1/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:22 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 4
Content-Type: text/plain

RED
$ curl -si -X PUT -d RED $BASE_URL/api/v1/status/
HTTP/1.1 204 No Content
Date: Mon, 18 Aug 2014 18:27:22 GMT
Server: Apache/2.4.7 (Ubuntu)
Content-Length: 0
Content-Type: text/plain

$ curl -si -H "Accept: application/json" http://localhost/~colin/api/v3/status/
HTTP/1.1 200 OK
Date: Mon, 18 Aug 2014 18:27:22 GMT
Server: Apache/2.4.7 (Ubuntu)
ETag: 620e41f9a45c62acb7b0ef0566b4e9ac911f4244
Transfer-Encoding: chunked
Content-Type: application/json

{"status": "RED"}
$ curl -si -H "Accept: application/json" -H "If-None-Match: 620e41f9a45c62acb7b0ef0566b4e9ac911f4244" http://localhost/~colin/api/v3/status/
HTTP/1.1 304 Not Modified
Date: Mon, 18 Aug 2014 18:27:57 GMT
Server: Apache/2.4.7 (Ubuntu)

$ 
```
