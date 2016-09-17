"""
Start the echo server on login.
"""

import sys
import os
import threading

from six.moves import BaseHTTPServer

import xbmc
import xbmcaddon

sys.path.append(os.path.join(os.path.dirname(__file__), 'httpd-echo'))
import httpdecho  # noqa

ADDON = xbmcaddon.Addon()


def main():
    """
    Start the echo server on login.
    """

    httpd = BaseHTTPServer.HTTPServer(
        ('localhost', int(ADDON.getSetting("port"))),
        httpdecho.EchoHTTPRequestHandler)
    httpd_thread = threading.Thread(target=httpd.serve_forever)
    httpd_thread.start()

    monitor = xbmc.Monitor()
 
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break

    httpd.shutdown()
    httpd.server_close()


if __name__ == '__main__':
    main()
