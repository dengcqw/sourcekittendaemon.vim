import json
import re
import urllib2
import vim
import threading


class SourceKittenDaemon(object):
    def __init__(self, port):
        self.__port = port

    def complete(self, prefix, path, completePart, offset):
        request = urllib2.Request("http://localhost:%d/complete" % self.__port)
        request.add_header("X_PATH", path)
        request.add_header("X_OFFSET", offset)
        request.add_header("X_Cachekey", completePart)
        request.add_header("X_Prefix", prefix)
        response = urllib2.urlopen(request).read()
        return response

class SourceKittenDaemonVim(object):
    def __init__(self, port=8080):
        self.__daemon = SourceKittenDaemon(port)

    def complete(self, prefix, path, completePart, offset):
        try:
            if offset == 0:
                vim.command('let s:result = ' + str([]))
                return
            response = self.__daemon.complete(prefix, path, completePart, offset)
            vim.command('let s:result = ' + str(response))
        except urllib2.HTTPError, error:
            vim.command("echoerr " + error)
