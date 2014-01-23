cluster-monitor
===============

James Mithen  
j.mithen@surrey.ac.uk

![](https://raw.github.com/jpmit/cluster-monitor/pic.png)

This is a simple webapp, written in Python/Javascript, for easy
monitoring of cluster computer jobs (specifically for the Sun Grid
Engine) using a web browser.  

The main page (files/monitor.html) polls the web server (server.py)
using AJAX.  When it receives a request, the server returns
information on the running jobs from a remote machine (to which the
server maintains an SSH connection).  The server is written in Python,
and shows how easy it is to build a (very basic) webserver in Python -
the required functionality is part of the standard library.  NB: The
server is not for production use - it is intended to be used on a
local machine.

Requirements
-------------
* Python2.x
* paramiko (used for SSH, see http://www.lag.net/paramiko/)

Usage
------

To run, type

    $ python server.py
Then use a web browser to navigate to http://127.0.0.1:8080/monitor.html

Note that you will need to modify the name of the machine (MACHINE_NAME in server.py)

Todo 
---- 

* It would be easy (and maybe useful) to modify the application to
  display different summary statistics on the cluster usage.
