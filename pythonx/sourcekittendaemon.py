import json
import re
import urllib2
import vim
import threading


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
        self._lock = threading.Lock()
        self._currentSession = ""

    def complete(self, prefix, path, completePart, offset, completeType):
        self._lock.acquire()
        if self._currentSession == self.calcSession(prefix, path, completePart, offset, completeType):
            self._lock.release()
            return
        self._lock.release()

        t = threading.Thread(target=self.complete_thread, args=(prefix, path, completePart, offset, completeType), name='thread')
        t.start()
        t.join()

    def complete_thread(self, prefix, path, completePart, offset, completeType):
        try:
            if offset == 0:
                vim.command('let s:result = ' + str([]))
                return
            cls = SourceKittenDaemonVim
            response = self.__daemon.complete(prefix, path, completePart, completeType, offset)
            self._lock.acquire()
            self._currentSession = ""
            self._lock.release()
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

    def calcSession(self, prefix, path, completePart, offset, completeType):
        return path+str(offset)+completePart

# if __name__=='__main__':
    # SourceKittenDaemonVim().complete("1","1","1","1","1")
