#!/usr/bin/env python

import traceback
import urllib2

DEMO_URL = 'https://www.google.com/'
# TODO Use Beautiful Soup to replace hrefs on the page so that relative paths resolve properly.
# TODO Test against something more interesting, like https://www.fortify.net/sslcheck.html

def application(environ, start_response):
    try:
        path = environ.get('PATH_INFO', '')
        if path == '/':
            start_response('200 OK', [('Content-Type', 'text/html')])
            return ['<html><body><a href="https://github.com/mattbornski/Python-WSGI-Proxy"><h1>Python WSGI Proxy</h1></a><p>For example:<br><a href="/' + DEMO_URL + '">http://proxy.bornski.com/' + DEMO_URL + '</a></p><p style="background-color:yellow"><blink><marquee><h3 style="color:red">Do not use this proxy to access sensitive HTTPS resources.  There is no encryption from your computer to this proxy.  This warning is extremely obnoxious so that you remember that I warned you.</h3></marquee></blink></p></body></html>']
        elif path.startswith('/http://') or path.startswith('/https://'):
            response = urllib2.urlopen(path.lstrip('/'))
            start_response(str(response.code), [('Content-Type', response.headers.get('Content-Type', 'text/plain'))])
            return [response.read()]
        else:
            raise ValueError('unknown protocol')
    except ValueError:
        start_response('404 Not Found', [])
        return []
    except Exception:
        start_response('500 Internal Server Error', [('Content-Type', 'text/html')])
        return ['<html><body><pre>GET ' + environ.get('PATH_INFO', '') + ' failed\n\n' + traceback.format_exc() + '</pre></body></html>']