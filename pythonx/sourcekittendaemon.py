import json
import re
import urllib2
import vim


class SourceKittenDaemon(object):
    def __init__(self, port):
        self.__port = port

    def complete(self, path, offset, completePart):
        request = urllib2.Request("http://localhost:%d/complete" % self.__port)
        request.add_header("X-Path", path)
        request.add_header("X-Offset", offset)
        request.add_header("X-Cachekey", completePart)
        response = urllib2.urlopen(request).read()
        return json.loads(response)


class SourceKittenDaemonVim(object):
    # TODO: add token jump
    __token_regexs = []#[re.compile("<#T##|##([^#].*)#>"), re.compile("#>")]
    # <#T##dic: [String : AnyObject]##[String : AnyObject]#>
    # <#T##allocator: CFAllocator!##CFAllocator!#>, <#T##localeID: CFLocaleIdentifier!##CFLocaleIdentifier!#>

    def __init__(self, port=8085):
        self.__daemon = SourceKittenDaemon(port)

    def complete(self, prefix, path, completePart, offset):
        try:
            cls = SourceKittenDaemonVim
            response = self.__daemon.complete(path, offset, completePart)
            completions = [
                x for x in map(cls.convert_to_completions, response)
                    if x and SourceKittenDaemonVim.matches(prefix, x)]
            vim.command('let s:result = ' + str(completions))
        except urllib2.HTTPError, error:
            vim.command("echoerr " + error)

    @classmethod
    def convert_to_completions(cls, response):
        try:
            return {
                "word": cls.remove_tokens(str(response["sourcetext"])),
                "abbr": str(response["name"]),
            }
        except KeyError:
            return None

    @classmethod
    def remove_tokens(cls, string):
        result = string
        for regex in cls.__token_regexs:
            result = re.sub(regex, "", result)
        return result

    @classmethod
    def matches(cls, prefix, dictionary):
        if not prefix:
            return True
        word = dictionary["word"]
        return word.startswith(prefix)
