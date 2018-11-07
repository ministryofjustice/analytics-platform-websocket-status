# Web Socket Status Page
[![Docker Repository on Quay](https://quay.io/repository/mojanalytics/websocket-status/status "Docker Repository on Quay")](https://quay.io/repository/mojanalytics/websocket-status)

A quick and dirty tool for checking websockets work

Due to strange network configurations we sometimes see users who can't use
jupyter or rstudio/shiny-apps. This is usually because of a problem with their
network setup. This is a service we can deploy and point their IT helpdesk to so
they can see the problem (because they can't login to the platform)

This will set up a server that sends the current time to any connected websockets
once a second and a webpage that will try to connect 25 websockets to that server.
The page will display the number of connected sockets and will tell you when all 25
are connected successfully.

## Installation and running locally
* create a virtualenv
* `pip install -r requirements.txt`
* `DEBUG=1 python server.py`

It will listen on port 8000.

## Running in docker
* `docker built . -t websocket-status`
* `docker run --rm -it websocket-status -P`



