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


class StupidHTTPRequestHandler(httpdecho.EchoHTTPRequestHandler):
    httpdecho.EchoHTTPRequestHandler.__doc__

    log_level = xbmc.LOGDEBUG

    def _log(self, format, args, level=None):
        """
        Common logging system call.
        """
        if level is None:
            level = self.log_level
        xbmc.log(
            "metadata.movie.stupid: %s - - [%s] %s\n" % (
                self.client_address[0], self.log_date_time_string(),
                format % args),
            level)

    def log_message(self, format, *args):
        """
        Send log messages to the logging module instead of stderr.
        """
        self._log(format, args)

    def log_error(self, format, *args):
        """
        Log at the correct level.
        """
        self.log_message(format, args, level=xbmc.LOGERROR)


def main():
    """
    Start the echo server on login.
    """

    httpd = BaseHTTPServer.HTTPServer(
        ('localhost', int(ADDON.getSetting("port"))),
        StupidHTTPRequestHandler)
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
