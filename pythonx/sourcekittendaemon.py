import json
import re
import urllib2
import vim


class SourceKittenDaemon(object):
    def __init__(self, port):
        self.__port = port

    def complete(self, prefix, path, completePart, completeType, offset):
        request = urllib2.Request("http://localhost:%d/complete" % self.__port)
        request.add_header("X-Path", path)
        request.add_header("X-Offset", offset)
        request.add_header("X-Cachekey", completePart)
        request.add_header("X-Type", completeType)
        request.add_header("X-Prefix", prefix)
        response = urllib2.urlopen(request).read()
        return response
        # return json.loads(response)


class SourceKittenDaemonVim(object):
    def __init__(self, port=8080):
        self.__daemon = SourceKittenDaemon(port)

    def complete(self, prefix, path, completePart, offset, completeType):
        try:
            if offset == 0:
                vim.command('let s:result = ' + str([]))
                return
            cls = SourceKittenDaemonVim
            response = self.__daemon.complete(prefix, path, completePart, completeType, offset)
            vim.command('let s:result = ' + str(response))
            # completions = [ x for x in map(cls.convert_to_completions, response) ]
            # vim.command('let s:result = ' + str(completions))
        except urllib2.HTTPError, error:
            vim.command("echoerr " + error)

    @classmethod
    def convert_to_completions(cls, response):
        try:
            return {
                "word": str(response[0]),
                "abbr": str(response[1]),
            }
        except KeyError:
            return None
